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
  













// require.config({
//     paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.23.0/min/vs" },
//   });
  
//   require(["vs/editor/editor.main"], function () {
//     monaco.editor.defineTheme("vs-dark", {
//       base: "vs-dark",
//       inherit: true,
//       rules: [],
//       colors: {},
//     });
  
//     monaco.editor.setTheme("vs-dark");
  
//     var htmlEditor = monaco.editor.create(
//       document.getElementById("htmlEditor"),
//       {
//         value:
//           '<html>\n\t<head>\n\t\t<style>\n\t\t\tbody {\n\t\t\t\tfont-family: Arial, sans-serif;\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n\t\t<h1>Hello, world!</h1>\n\t</body>\n</html>',
//         language: "html",
//       }
//     );
  
//     var cssEditor = monaco.editor.create(document.getElementById("cssEditor"), {
//       value:
//         'body {\n\tfont-family: Arial, sans-serif;\n\tbackground-color: #f0f0f0;\n}\n\nh1 {\n\tcolor: #333;\n\tmargin: 20px;\n}',
//       language: "css",
//     });
  
//     var jsEditor = monaco.editor.create(document.getElementById("jsEditor"), {
//       value: 'console.log("Hello, world!");',
//       language: "javascript",
//     });
  
//     var runButton = document.getElementById("runButton");
//     var output = document.getElementById("output");
  
//     runButton.addEventListener("click", function () {
//       var userHtmlCode = htmlEditor.getValue();
//       var userCssCode = cssEditor.getValue();
//       var userJsCode = jsEditor.getValue();
  
//       // Save the user's code to the server
//       saveUserCodes(userHtmlCode, userCssCode, userJsCode);
  
//       var combinedCode = `
//         ${userHtmlCode}
//         <style>${userCssCode}</style>
//         <script>${userJsCode}</script>
//       `;
      
  
//       try {
//         output.textContent = ""; // Clear previous output
//         var iframe = document.createElement("iframe");
//         iframe.style.border = "none";
//         iframe.style.width = "100%";
//         iframe.style.height = "100%";
//         iframe.srcdoc = combinedCode;
//         output.appendChild(iframe);
//       } catch (error) {
//         output.textContent = "Error:\n" + error;
//       }
//     });

  
//     // Fetch and load user's code from the server
//     fetchUserCodes(function (data) {
//       htmlEditor.setValue(data.html_code);
//       cssEditor.setValue(data.css_code);
//       jsEditor.setValue(data.js_code);
//     });
//   });

  
//   function fetchUserCodes() {
//     fetch("/get_user_codes/")  // URL to fetch user codes
//       .then((response) => response.json())
//       .then((data) => {
//         const { html_code, css_code, js_code } = data;

//         // Initialize editors with fetched codes
//         htmlEditor.setValue(html_code);
//         cssEditor.setValue(css_code);
//         jsEditor.setValue(js_code);
//       });
//   }

//   function saveUserCodes(htmlCode, cssCode, jsCode) {
//     fetch("/save_user_codes/", {  // URL to save user codes
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": getCookie("csrftoken"),
//       },
//       body: JSON.stringify({
//         html_code: htmlCode,
//         css_code: cssCode,
//         js_code: jsCode,
//       }),
//     });
//   }
  
  
//   function getCookie(name) {
//     var value = "; " + document.cookie;
//     var parts = value.split("; " + name + "=");
//     if (parts.length === 2) return parts.pop().split(";").shift();
//   }
  


// require.config({
//   paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.23.0/min/vs" },
// });

// require(["vs/editor/editor.main"], function () {
//   monaco.editor.defineTheme("vs-dark", {
//     base: "vs-dark",
//     inherit: true,
//     rules: [],
//     colors: {},
//   });

//   monaco.editor.setTheme("vs-dark");

//   var defaultHtmlCode = [
//     "<html>",
//     "\t<head>",
//     "\t\t<style>",
//     "\t\t\tbody {",
//     "\t\t\t\tfont-family: Arial, sans-serif;",
//     "\t\t\t}",
//     "\t\t</style>",
//     "\t</head>",
//     "\t<body>",
//     "\t\t<h1>Hello, world!</h1>",
//     "\t</body>",
//     "</html>",
//   ].join("\n");

//   var defaultCssCode = [
//     "body {",
//     "\tfont-family: Arial, sans-serif;",
//     "\tbackground-color: #f0f0f0;",
//     "}",
//     "",
//     "h1 {",
//     "\tcolor: #333;",
//     "\tmargin: 20px;",
//     "}",
//   ].join("\n");

//   var defaultJsCode = 'console.log("Hello, world!");';

//   var htmlEditor = monaco.editor.create(document.getElementById("htmlEditor"), {
//     value: localStorage.getItem("userHtmlCode") || defaultHtmlCode,
//     language: "html",
//   });

//   var cssEditor = monaco.editor.create(document.getElementById("cssEditor"), {
//     value: localStorage.getItem("userCssCode") || defaultCssCode,
//     language: "css",
//   });

//   var jsEditor = monaco.editor.create(document.getElementById("jsEditor"), {
//     value: localStorage.getItem("userJsCode") || defaultJsCode,
//     language: "javascript",
//   });

//   var runButton = document.getElementById("runButton");
//   var output = document.getElementById("output");

//   runButton.addEventListener("click", function () {
//     var userHtmlCode = htmlEditor.getValue();
//     var userCssCode = cssEditor.getValue();
//     var userJsCode = jsEditor.getValue();

//     // Save the user's code to Local Storage
//     localStorage.setItem("userHtmlCode", userHtmlCode);
//     localStorage.setItem("userCssCode", userCssCode);
//     localStorage.setItem("userJsCode", userJsCode);

//     var combinedCode = `
//                     ${userHtmlCode}
//                     <style>${userCssCode}</style>
//                     <script>${userJsCode}</script>
//                 `;

//     try {
//       output.textContent = ""; // Clear previous output
//       var iframe = document.createElement("iframe");
//       iframe.style.border = "none";
//       iframe.style.width = "100%";
//       iframe.style.height = "100%";
//       iframe.srcdoc = combinedCode;
//       output.appendChild(iframe);
//     } catch (error) {
//       output.textContent = "Error:\n" + error;
//     }
//   });
// });


