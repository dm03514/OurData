<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Logged In</%block>

<%block name="navigation"></%block>

<%block name="content">
    <h2>Datasets</h2>
    <ul>
        % for dataset in datasets:
            <li>
                <a href="/dataset/get/${dataset.slug}">
                    ${dataset}
                </a>
            </li>
        % endfor
    </ul>
    <h2>Users</h2>
    <ul>
        % for user in users:
            <li>
                % if user.is_admin:
                    ${user} - <b>is admin</b>
                % else:
                    <a href="${request.route_url('edit_permissions', user_id=user.id_as_str)}">${user}</a>
                % endif
            </li>
        % endfor
    </ul>
</%block>

<%block name="sidebar">
    <h3>Links</h3>

    <form action="/dataset/create" method="POST">
        <label>Create new dataset</label>
        <input type="text" name="title" />
        <input type="submit" value="Create" />
    </form>

    <ul>
        <li></li>
        <li></li>
    </ul>
</%block>
