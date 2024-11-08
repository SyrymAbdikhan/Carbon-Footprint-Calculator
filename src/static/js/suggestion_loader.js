
var suggestion = document.querySelector('#suggestion');
var btn = document.querySelector('#generate-suggestion');
var spinner = document.querySelector('#spinner');
var url = new URL(window.location.href);
var result_id = url.searchParams.get("result_id");

btn.addEventListener('click', () => {
    btn.classList.add("pointer-events-none");
    btn.classList.remove("hover:bg-blue-500");
    spinner.style.display = 'block';

    fetch(`/get_suggestion/?result_id=${result_id}`)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            if (data.status_code == 0) {
                suggestion.textContent = data.response;
                prettify(suggestion);
            } else {
                alert(data.response);
            }
        })
        .catch(() => {
            alert('oblom');
            btn.classList.remove("pointer-events-none");
            btn.classList.add("hover:bg-blue-500");
            spinner.style.display = 'none';
        });
});

btn.click();
