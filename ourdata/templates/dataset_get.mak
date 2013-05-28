<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Logged In</%block>

<%block name="navigation"></%block>

<%block name="content">
    <h2>${dataset.title}</h2>
    % if request.user.is_admin:
        % for field in dataset.fields:
            ${field}
        % endfor
        <input type="
    % endif
</%block>

<%block name="sidebar">
    <h3>Links</h3>
    % if request.user.is_admin:
        <form action="/dataset/create" method="POST">
            <label>Create new dataset</label>
            <input type="text" name="title" />
            <input type="submit" value="Create" />
        </form>
    % endif
    <ul>
        <li></li>
        <li></li>
    </ul>
</%block>
