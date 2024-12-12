
var suggestion = document.querySelector('#suggestion');
var btn = document.querySelector('#generate-suggestion');
var spinner = document.querySelector('#spinner');

var href = window.location.href;
var result_id = href.substring(href.lastIndexOf('/') + 1);

function spinner_show() {
  btn.classList.add("pointer-events-none");
  btn.classList.remove("hover:bg-blue-500");
  spinner.style.display = 'block';
}

function spinner_hide() {
  btn.classList.remove("pointer-events-none");
  btn.classList.add("hover:bg-blue-500");
  spinner.style.display = 'none';
}

btn.addEventListener('click', () => {
  spinner_show();

  fetch(`/api/get_suggestion/${result_id}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.status_code == 0) {
        suggestion.textContent = data.response;
        prettify(suggestion);
      } else {
        alert(data.response);
        spinner_hide();
      }
    })
    .catch((e) => {
      console.log(e);
      spinner_hide();
    });
});

btn.click();
