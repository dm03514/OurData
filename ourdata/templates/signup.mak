<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Signup!</%block>

<%block name="content">
    <h2>Signup</h2>
    <form id="signup" method="POST" action="/signup">
        <div class="form_settings">
            <p>
                <span>First Name</span>
                <input type="text" name="first_name" id="first_name" />
            </p>
            <p>
                <span>Last Name</span>
                <input type="text" name="last_name" id="last_name" />
            </p>
            <p>
                <span>Email</span>
                <input type="text" name="email" id="email" />
            </p>
            <p>
                <span>Password</span>
                <input type="text" name="password" id="password" />
            </p>
            <p>
                <span></span>
                <input type="submit" class="submit" value="Signup!" />
            </p>
            
        </div>
    </form>
</%block>
