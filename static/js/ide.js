require.config({
    paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.23.0/min/vs" },
  });
  
  require(["vs/editor/editor.main"], function () {
    monaco.editor.defineTheme("vs-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [],
      colors: {},
    });
  
    monaco.editor.setTheme("vs-dark");
  
    var htmlEditor = monaco.editor.create(
      document.getElementById("htmlEditor"),
      {
        language: "html",
      }
    );
  
    var cssEditor = monaco.editor.create(document.getElementById("cssEditor"), {
      language: "css",
    });
  
    var jsEditor = monaco.editor.create(document.getElementById("jsEditor"), {
      language: "javascript",
    });
  
    var runButton = document.getElementById("runButton");
    var output = document.getElementById("output");
  
    runButton.addEventListener("click", function () {
      var userHtmlCode = htmlEditor.getValue();
      var userCssCode = cssEditor.getValue();
      var userJsCode = jsEditor.getValue();
  
      // Save the user's code to the server
      saveUserCodes(userHtmlCode, userCssCode, userJsCode);
  
      var combinedCode = `
        ${userHtmlCode}
        <style>${userCssCode}</style>
        <script>${userJsCode}</script>
      `;
  
      try {
        output.textContent = ""; // Clear previous output
        var iframe = document.createElement("iframe");
        iframe.style.border = "none";
        iframe.style.width = "100%";
        iframe.style.height = "100%";
        iframe.srcdoc = combinedCode;
        output.appendChild(iframe);
      } catch (error) {
        output.textContent = "Error:\n" + error;
      }
    });
  
    // Fetch and load user's code from the server
    fetchUserCodes(function (data) {
      htmlEditor.setValue(data.html_code);
      cssEditor.setValue(data.css_code);
      jsEditor.setValue(data.js_code);
    });
  });
  
  function fetchUserCodes(callback) {
    fetch("/get_user_codes/")  // URL to fetch user codes
      .then((response) => response.json())
      .then((data) => {
        const { html_code, css_code, js_code } = data;
  
        // Call the callback function with the fetched codes
        callback({ html_code, css_code, js_code });
      });
  }
  
  function saveUserCodes(htmlCode, cssCode, jsCode) {
    fetch("/save_user_codes/", {  // URL to save user codes
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        html_code: htmlCode,
        css_code: cssCode,
        js_code: jsCode,
      }),
    });
  }
  
  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  


  require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.24.0/min/vs' }});
  require(['vs/editor/editor.main'], function() {
      const editor = monaco.editor.create(document.getElementById('editor'), {
          value: 'print("Hello, world!")',
          language: 'python',
      });

      const runButton = document.getElementById('run-button');
      const consoleDiv = document.getElementById('console');

      runButton.addEventListener('click', function() {
          const code = editor.getValue();

          // Send the code to the backend for execution
          const socket = new WebSocket('ws://your-server-url/code_execution/');
          socket.onopen = function(event) {
              socket.send(JSON.stringify({ code: code }));
          };

          // Receive the result from the backend and display it in the console
          socket.onmessage = function(event) {
              const data = JSON.parse(event.data);
              consoleDiv.textContent = data.result;
          };
      });
  });
