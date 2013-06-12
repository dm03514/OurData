<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Logged In</%block>

<%block name="navigation"></%block>

<%block name="content">
    % if credentials:
        <table>
            <tr>
                <th>Dataset ID</th>
                <th>Public Key</th>
                <th>Private Key</th>
            </tr>

            % for credential in credentials:
                <td>
                    ${credential.dataset_id}
                </td>
                <td>${credential.public_key}</td>
                <td>${credential.private_key}</td>
            % endfor
        </table>
    % endif
</%block>

<%block name="sidebar"></%block>
