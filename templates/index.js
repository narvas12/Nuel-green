class Header extends HTMLElement {
    constructor() {
      super();
    }
  
    connectedCallback() {
      this.innerHTML = `
      <header class="flex justify-between items-center w-full bg-black py-2 h-[50px] px-6">
      <div class="w-[300px] border border-gray-600 rounded-lg flex items-center gap-2 justify-between p-2 ">
        <img src='images/logo.png' alt='' class='logo' />
      </div>
    
      <div class="flex gap-4 items-center ml-4">
        <div>
          <i class="fa-solid fa-people-group text-white"></i>
        </div>
        <button class='text-white blue px-4 py-1 rounded-lg'>
          Login
        </button>
      </div>
    </header>
      `;
    }
  }
  
  customElements.define('header-component', Header);