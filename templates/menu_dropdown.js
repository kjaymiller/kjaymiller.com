<script>
  const navBurger = document.querySelector('.navbar-burger');

  navBurger.addEventListener('click', () => {

    // Get the target from the "data-target" attribute
    const target = navBurger.dataset.target;

    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
     navBurger.classList.toggle('is-active');

    const navMenu = document.querySelector('.navbar-menu');
    console.log(navMenu);
    navMenu.classList.toggle('is-visible');
  });
</script>
