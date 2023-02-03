

(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

 

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable);
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }


  var imgWrap = "";
  var imgArray = [];

  $('.upload__inputfile').each(function () {
    $(this).on('change', function (e) {
      imgWrap = $(this).closest('.upload__box').find('.upload__img-wrap');
      var maxLength = $(this).attr('data-max_length');

      var files = e.target.files;
      var filesArr = Array.prototype.slice.call(files);
      var iterator = 0;
      filesArr.forEach(function (f, index) {

        if (!f.type.match('image.*')) {
          return;
        }

        if (imgArray.length > maxLength) {
          return false
        } else {
          var len = 0;
          for (var i = 0; i < imgArray.length; i++) {
            if (imgArray[i] !== undefined) {
              len++;
            }
          }
          if (len > maxLength) {
            return false;
          } else {
            imgArray.push(f);

            var reader = new FileReader();
            reader.onload = function (e) {
              var html = "<div class='upload__img-box'><div style='background-image: url(" + e.target.result + ")' data-number='" + $(".upload__img-close").length + "' data-file='" + f.name + "' class='img-bg'><div class='upload__img-close'></div></div></div>";
              imgWrap.append(html);
              iterator++;
            }
            reader.readAsDataURL(f);
          }
        }
      });
    });
  });

  $('body').on('click', ".upload__img-close", function (e) {
    var file = $(this).parent().data("file");
    for (var i = 0; i < imgArray.length; i++) {
      if (imgArray[i].name === file) {
        imgArray.splice(i, 1);
        break;
      }
    }
    $(this).parent().parent().remove();
  });




    

})();

function loaddata(){
  
  var ys = document.getElementById("yearstart");
  var ms = document.getElementById("monthstart");
  var ds = document.getElementById("daystart");

  var ye = document.getElementById("yearend");
  var me = document.getElementById("monthend");
  var de = document.getElementById("dayend");



  let option3 = '<option value="" selected disabled>Choose</option>';

  for (let i = 0; i < 25; i++) {
    // value day number with 0. 01 02 03 04..
    let day = (i <= 9) ? '0' + i : i;

    // or value day number 1 2 3 4..
    // let day = i;
    if (i == 24){
      option3 += '<option value=23:59>23:59</option>';
    }else{
      option3 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
      option3 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
    }
  }
  document.getElementById("timestart").innerHTML = option3;
  document.getElementById("timeend").innerHTML = option3;
  


  let year_start = (new Date).getFullYear();
  let year_end = (new Date).getFullYear() + 1; // current year
  let year_selected = (new Date).getFullYear();

    let option = '';

    for (let i = year_start; i <= year_end; i++) {
        let selected = (i === year_selected ? ' selected' : '');
        option += '<option value="' + i + '"' + selected + '>' + i + '</option>';
    }

    ys.innerHTML = option;
    ye.innerHTML = option;

    var month_selected = (new Date).getMonth(); // current month
    var option1 = '';

    for (let i = 0; i < 12; i++) {
        let month_number = (i + 1);

        // value month number with 0. [01 02 03 04..]
        let month = (month_number <= 9) ? '0' + month_number : month_number;

        // or value month number. [1 2 3 4..]
        // let month = month_number;

        // or value month names. [January February]
        // let month = months[i];

        let selected = (i === month_selected ? ' selected' : '');
        option1 += '<option value="' + month + '"' + selected + '>' + month + '</option>';
    }
    ms.innerHTML = option1;
    me.innerHTML = option1;


    let day_selected = (new Date).getDate(); // current day
    let option2 = '';

    for (let i = 1; i < 32; i++) {
        // value day number with 0. 01 02 03 04..
        let day = (i <= 9) ? '0' + i : i;

        // or value day number 1 2 3 4..
        // let day = i;

        let selected = (i === day_selected ? ' selected' : '');
        option2 += '<option value="' + day + '"' + selected + '>' + day + '</option>';
    }
    ds.innerHTML = option2;
    de.innerHTML = option2;

}



function checkdate(){
  var ys = document.getElementById("yearstart");
  var ms = document.getElementById("monthstart");
  var ds = document.getElementById("daystart");

  var ye = document.getElementById("yearend");
  var me = document.getElementById("monthend");
  var de = document.getElementById("dayend");

  let startyear = parseInt(ys.value, 10),
  startmonth = parseInt(ms.value, 10),
  startday = parseInt(ds.value, 10);

  let endyear = parseInt(ye.value, 10),
  endmonth = parseInt(me.value, 10),
  endday = parseInt(de.value, 10);

  const startdate = new Date([startyear, startmonth, startday].join('-'));
  const enddate = new Date([endyear, endmonth, endday].join('-'));

  
  const diffTime = Math.abs(enddate - startdate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  console.log(diffDays);

  if (diffDays >= 7){
    document.getElementById("javachanged").style.display = "block";
  }else{
    document.getElementById("javachanged").style.display = "none";
  }

}

function checkstatus(){
  let status = document.getElementById("status").value;
  if (status == "worktime"){
    
    let option2 = '<option value="" selected disabled>Choose</option>';
    let option1 = '<option value="" selected disabled>Choose</option>';

    for (let i = 0; i < 25; i++) {
      // value day number with 0. 01 02 03 04..
      let day = (i <= 9) ? '0' + i : i;

      // or value day number 1 2 3 4..
      // let day = i;
      if (i == 24){
        option1 += '<option value=23:59>23:59</option>';
        option2 += '<option value=23:59>23:59</option>';
        
      }else{
        option1 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
        option1 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
        option2 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
        option2 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
      }
    }
    document.getElementById("timestartnew").innerHTML = option1;
    document.getElementById("timeendnew").innerHTML = option2;
    document.getElementById("timechange").style.display = "block";
    document.getElementById("timenone").style.display = "none";
  }
  else if (status == "halfday"){
    let option3 = '<option value="" selected disabled>Choose</option>';

    for (let i = 0; i < 25; i++) {
      // value day number with 0. 01 02 03 04..
      let day = (i <= 9) ? '0' + i : i;

      // or value day number 1 2 3 4..
      // let day = i;
      if (i == 24){
        option3 += '<option value=23:59>23:59</option>';
      }else{
        option3 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
        option3 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
      }
    }
    document.getElementById("timeendnew2").innerHTML = option3;
    document.getElementById("timenone").style.display = "block";
    document.getElementById("timechange").style.display = "none";
  }
  else{
    document.getElementById("timenone").style.display = "none";
    document.getElementById("timechange").style.display = "none";
  }
}


/**
   * check password
   */

var password = document.getElementById("newPassword")
  , confirm_password = document.getElementById("renewPassword");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;


