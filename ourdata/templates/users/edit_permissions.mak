<%inherit file="ourdata:templates/base.mak" />

<%block name="title">User Permissions Edit</%block>

<%block name="navigation"></%block>

<%block name="content">
    % if user_credentials:
        <table>
            <tr>
                <th>Dataset ID</th>
                <th>Is Active?</th>
                <th>Approval Datetime</th>
            </tr>
            % for credential in user_credentials:
                <tr>
                    <td>${credential.dataset_id}</td>
                    <td>${credential.is_active}</td>
                    <td>${credential.approval_datetime}</td>
                </tr>
            % endfor
        </table>
    % endif

    <form action="${request.route_url('add_credentials', user_id=user_id)}" method="post">
        <h2>Add credential, Give user access to API</h2>
        <select name="dataset_id">
            % for dataset in all_datasets:
                <option value="${dataset.id}">${dataset.title}</option>
            % endfor
        </select>
        <input type="submit" value="Add Credential" />
    </form>
</%block>
