# your_app_name/middleware.py
import time
from user_agents import parse
from channels.layers import get_channel_layer
from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith('/ws/'):  # Handle WebSocket connections
            channel_name = request.GET.get('channel_name')  # Get channel_name from the WebSocket query parameter
            return self.handle_websocket(request, channel_name)

        # Record the start time for the request
        request.start_time = time.time()

        response = self.get_response(request)

        # Calculate the time spent on the website
        end_time = time.time()
        elapsed_time = end_time - request.start_time

        # Get the client information
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        client_info = {
            'ip_address': self.get_client_ip(request),
            'browser': user_agent.browser.family,
            'os': user_agent.os.family,
            'device': user_agent.device.family,
            'time_spent': elapsed_time,
        }

        # Save the visitor information to the database
        self.track_visitor(client_info)

        return response

    def handle_websocket(self, request, channel_name):
        # Handle WebSocket connections here
        channel_layer = get_channel_layer()
        user = request.user if request.user.is_authenticated else None

        async def connect():
            request.websocket.connect_time = time.time()
            await self.send_websocket_data(channel_layer, 'connect', user, channel_name)

        async def disconnect():
            # Calculate the time spent on the website during the WebSocket session
            connect_time = getattr(request.websocket, 'connect_time', None)
            if connect_time is not None:
                disconnect_time = time.time()
                elapsed_time = disconnect_time - connect_time

                # Update or create the Visitor record
                self.track_visitor({
                    'ip_address': self.get_client_ip(request),
                    'browser': 'WebSocket',  # Use a placeholder value for WebSocket sessions
                    'os': 'WebSocket',  # Use a placeholder value for WebSocket sessions
                    'device': 'WebSocket',  # Use a placeholder value for WebSocket sessions
                    'time_spent': elapsed_time,
                })

            await self.send_websocket_data(channel_layer, 'disconnect', user, channel_name)

        async def receive(message):
            pass  # You can handle WebSocket messages if needed

        return connect, disconnect, receive

    async def send_websocket_data(self, channel_layer, event_type, user, channel_name):
        # Send WebSocket data to update user status
        if user and channel_name:
            data = {
                'type': event_type,
                'user_id': user.id,
            }
            await channel_layer.group_add(user.id, channel_name)
            await channel_layer.group_send(user.id, data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

        
    def track_visitor(self, client_info):
        # Check if a record with the same IP address already exists
        existing_visitor = Visitor.objects.filter(ip_address=client_info['ip_address']).first()

        if existing_visitor:
            # Check if the browser or device is different
            if (
                existing_visitor.browser != client_info['browser']
                or existing_visitor.device != client_info['device']
            ):
                # Create a new record
                Visitor.objects.create(
                    ip_address=client_info['ip_address'],
                    browser=client_info['browser'],
                    os=client_info['os'],
                    device=client_info['device'],
                    time_spent=client_info['time_spent']
                )
            else:
                # Update the existing record with the new time spent
                existing_visitor.time_spent += client_info['time_spent']
                existing_visitor.save()
        else:
            # Create a new record
            Visitor.objects.create(
                ip_address=client_info['ip_address'],
                browser=client_info['browser'],
                os=client_info['os'],
                device=client_info['device'],
                time_spent=client_info['time_spent']
            )
