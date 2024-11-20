<template>
    <div class="mart-view">
      <Navbar />
      <EventBanner />  
    </div>
  </template>
  
  <script>
  import Navbar from '@/components/Navbar/MartNavbar.vue';
  import EventBanner from '@/components/EventBanner.vue';

  export default {
    name: 'MartView',
    components: {
      Navbar,
      EventBanner,
    },
  };
  </script>
  
  <style scoped>
  .home-view {
    width: 100%;
  }
  
  .banner-section {
    position: relative;
    text-align: center;
  }
  
  .banner-section img {
    width: 100%;
  }
  
  .banner-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
  }
  
  .popular-categories {
    padding: 20px;
  }
  
  .category-list {
    display: flex;
    justify-content: space-around;
  }
  
  .category-list > * {
    flex-basis: calc(100% / 5);
  }
  </style>