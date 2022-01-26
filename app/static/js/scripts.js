var all_cont = document.querySelectorAll('.card_contacts');

[].forEach.call( all_cont, function(el) {

    el.onclick = function(e) {
        console.log(el);
        var text = el.innerText;
        document.getElementById('srch').value = text;
        console.log(text);
    }
});

var all_author = document.querySelectorAll('.card_author');

[].forEach.call( all_author, function(el) {

    el.onclick = function(e) {
        console.log(el);
        var text = el.innerText;
        document.getElementById('srch').value = text;
        console.log(text);
    }
});

var all_exs = document.querySelectorAll('.exs');

[].forEach.call( all_exs, function(el) {

    el.onclick = function(e) {
        console.log(el);
        var text = el.innerText;
        document.getElementById('srch').value = text;
        console.log(text);
    }
});