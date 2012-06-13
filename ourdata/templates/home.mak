<%inherit file="ourdata:templates/base.mak" />

<%block name="title">OurData!</%block>


<%block name="content">
    <h1>Welcome!</h1>
    <p>Please Signup for an account, or login to the right.</p>
</%block>

<%block name="sidebar">
    <h2>Login</h2>
    <form id="login" method="POST" action="/login">
        <div class="form_settings">
            <p>
                <span>Email</span>
                <input type="text" name="email" id="email" />
            </p>
            <p>
                <span>Password</span>
                <input type="text" name="password" id="password" />
            </p>
            <p>
                <input type="submit" class="submit" value="Login!" />
            </p>
        </div>
    </form>

</%block>
