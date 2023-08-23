let arrow = document.querySelectorAll(".arrow");

for (let i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;
    // console.log(arrowParent)
    arrowParent.classList.toggle("showMenu");
  });
}
console.log()
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");

sidebarBtn.addEventListener("click", () => {
  console.log("closed");
  sidebar.classList.toggle("close");
});


 // Get all the module elements
 const modules = document.querySelectorAll('.module');

 // Add click event listeners to each module's title to toggle the dropdown
 modules.forEach((module) => {
     const arrowIcon = module.querySelector('.arrow');
     const moduleTitle = module.querySelector('.module-title');

     module.querySelector('.modules-title').addEventListener('click', () => {
         moduleTitle.classList.toggle('active');
     });
 });



 document.addEventListener("DOMContentLoaded", function () {
  const projectForm = document.getElementById("project-form");
  const projectFeedback = document.getElementById("project-feedback");

  projectForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(projectForm);

    try {
      const response = await fetch("{% url 'academy:user_dashboard' %}", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        projectFeedback.innerHTML = `Project submitted: <a href="${data.project_link}" target="_blank">${data.project_title}</a>`;
      } else {
        console.error("Response not OK:", response);
        projectFeedback.innerHTML = "Project submission failed.";
      }
    } catch (error) {
      console.error("Error occurred:", error);
      projectFeedback.innerHTML = "An error occurred while submitting the project.";
    }
  });

});





