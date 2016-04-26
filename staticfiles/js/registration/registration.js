(function() {
    if (!globals.authenticated) {
        if(globals.auth_form_submitted) {
            generateLogin();
            globals.selected = true;
        } else if(globals.member_form_submitted) {
            generateMemberForm();
            globals.selected = true;
        } else {
            var text = `<div class="row">
                        <div class="button-block">
                            <p>
                                <button class=" btn btn-default clickables" type='button'
                                        onclick="generateLogin()">Login
                                </button>
                                <span class="text">	&nbsp;	or 	&nbsp;  </span>
                                <button class="btn btn-default clickables" type='button' onclick="generateMemberForm()">
                                    Create a new account
                                </button>
                            </p>
                        </div>
                    </div>`;
            var placeholder = document.getElementById("placeholder");
            placeholder.innerHTML = text;
            globals.selected = false;
        }
    }

    if ((globals.err_msg).length > 0) {
        document.getElementById('warning-block').innerHTML =
            `<div class="warning">
                <div class="alert alert-danger">`
                    + globals.err_msg +
                `</div>
            </div>`;
        $('Form').css('margin-top', '-30px');
    }
})();

function generateLogin() {
    var placeholder = document.getElementById("placeholder");
    placeholder.innerHTML = globals.login;
    globals.selected = true;
}

function generateMemberForm() {
    var placeholder = document.getElementById("placeholder");
    placeholder.innerHTML = globals.member;
    globals.selected = true;
}

function submitForm() {
    if (globals.selected) {
        document.getElementById("Form").submit();
    } else {
        document.getElementById('warning-block').innerHTML =
            `<div class="warning">
                <div class="alert alert-danger">
                    <strong>Error: </strong> Select an Account option to sign in.
                </div>
            </div>`;
        $('Form').css('margin-top', '-30px');
    }
}
