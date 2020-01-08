const name = localStorage.getItem('username');

const dialog = document.getElementById('username-dialog');
//If the user has his/her name in the storage, let them see the page. Otherwise show the form.
// I display a layer on top of the content if the username does not exist.
if (name) {
    document.getElementById('username').textContent = name
    if (dialog) {
        document.getElementById('username-dialog').style.visibility = 'hidden';
    }
} else {
    if (dialog) {
        document.getElementById('username-dialog').style.visibility = 'visible';
    }
    const form = document.getElementById('username-form');
    form.addEventListener('submit', function() {
        let username = document.querySelector('input[name="username"]').value;
        localStorage.setItem('username', username);
    })
}

// used classname not to get "null" error in the homepage. Easier to check for the length of it.
//If the user is in detail page, fill in the username in the form, on page load.
const formUsername = document.querySelector('.form-username');
if (formUsername) {
    console.log('writing formusername')
    formUsername.value = name;
}


const changeUsernameButton = document.getElementById('change-username');
changeUsernameButton.addEventListener('click', function() {
    localStorage.clear();
    window.location.href = '/';
});



//Each comment has a reply button. Get them all.
const replyButton = document.querySelectorAll('.reply-button');
//make an array out of them to loop through
const buttonsArray = Array.from(replyButton);

//add event listener to buttons
buttonsArray.forEach(function(button) {
    // to be able to bind button to its own form so that each button will refer to it's form
    // I give them commom ids. one has dataset id the other has it's own id. But they are the same.
    let form = document.getElementById(button.dataset.id);
    let username = form.querySelector('.answer-username')
    //On page load, hide the form.
    form.style.display = 'none'
    //When clicked on the reply button, show the form.
    button.addEventListener('click', function() {
        form.style.display = 'block'
        //finally before submitting, set the username of the answer to the current user.
        username.value = localStorage.getItem('username');
    })
});
