$( document ).ready(function() {
    let arr = JSON.parse(localStorage.getItem('checked')) || [];
    arr.forEach(function (i) {
        $("."+i).css('color', 'green');
    })
});
