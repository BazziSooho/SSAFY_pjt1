<template>
    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-logo">
        </div>
  
        <!-- Navigation Links -->
        <ul class="navbar-links">
          <li><a href="#">빠른장보기</a></li>
          <li><a href="#">전단행사</a></li>
          <li><a href="#">PB상품관</a></li>
          <li><a href="#">베스트</a></li>
          <li><a href="#">근처 마트 찾기</a></li>
          <!-- 이벤트링크 추가할것 -->
          <li><a href="/savings/add">적금이율 이벤트</a></li> 
        </ul>
  
      </div>
    </nav>
  </template>
  
  <script>
  </script>
  
  <style scoped>
  .navbar {
    background-color: #fff;
    border-bottom: 1px solid #eee;
    padding: 10px 20px;
  }
  
  .navbar-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }
  
  .navbar-logo img {
    height: 40px;
  }
  
  .navbar-links {
    display: flex;
    list-style: none;
    gap: 20px;
  }
  
  .navbar-links li a {
    text-decoration: none;
    color: #333;
  }
  
  /* important 아이디가 있는 li 태그의 a 요소에만 스타일 적용 */
  #important a {
    color: #ff0000; /* 원하는 색상으로 변경 */
    font-weight: bold; /* 볼드체 적용 */
  }
  
  .navbar-actions {
    display: flex;
    gap: 10px;
  }
  
  .login-btn,
  .cart-btn {
    background-color: #4CAF50; /* 농협몰의 녹색 테마 */
    color: white;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
  }
  
  .login-btn:hover,
  .cart-btn:hover {
    background-color: #45a049; /* Hover 효과 */
  }
  </style>