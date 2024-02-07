const textElement = document.getElementById("typed-text");
const text = textElement.textContent;
textElement.textContent = ""; // Clear the text initially

let i = 0;
function typeText() {
  if (i < text.length) {
    textElement.textContent += text.charAt(i);
    i++;
    setTimeout(typeText, 100); // Adjust the speed by changing the timeout value (milliseconds)
  }
}

typeText(); // Start the typing animation

menuToggle = document.querySelector(".menuToggle");
header = document.querySelector("header");

menuToggle.addEventListener("click", function () {
  header.classList.toggle("active");
});

document.addEventListener("DOMContentLoaded", function () {
  // Get the hero_img element
  const heroImg = document.getElementById("heroImg");

  setTimeout(() => {
    
    heroImg.classList.add("slide-in");
  }, 500); // 500 milliseconds delay
});

document.querySelectorAll(".accordion-header").forEach((button) => {
  button.addEventListener("click", () => {
    const accordionContent = button.nextElementSibling;

    button.classList.toggle("active");

    if (button.classList.contains("active")) {
      accordionContent.style.maxHeight = accordionContent.scrollHeight + "px";
    } else {
      accordionContent.style.maxHeight = 0;
    }

    // Close other open accordion items
    document.querySelectorAll(".accordion-header").forEach((otherButton) => {
      if (otherButton !== button) {
        otherButton.classList.remove("active");
        otherButton.nextElementSibling.style.maxHeight = 0;
      }
    });
  });
});


window.addEventListener('scroll', () => {
  var reveals = document.querySelectorAll('#section');
  for (let i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var revealTop = reveals[i].getBoundingClientRect().top;
    var revealPoint = 150;

    if (revealTop < windowHeight - revealPoint) {
      if (!reveals[i].classList.contains('reveal')) {
        reveals[i].classList.add('reveal');
      }
    } else {
      reveals[i].classList.remove('reveal');
    }
  }
});



function updateCounter(counterId, maxCount) {
  const counterElement = document.getElementById(counterId);
  let count = parseInt(counterElement.innerText);

  // Check if the count is less than the specified maxCount
  if (count < maxCount) {
    count++;
    counterElement.innerText = (count > 1) ? count + '+': count;
  } else {
    // Reset the counter after reaching the maxCount
    setTimeout(() => {
      counterElement.innerText = '1';
    }, 1000);
  }
}

// Update each counter every 100 milliseconds with different max counts
setInterval(() => updateCounter('counter1', 1000), 1);
setInterval(() => updateCounter('counter2', 10), 100);
setInterval(() => updateCounter('counter3', 15), 100);