<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Logged In</%block>

<%block name="navigation"></%block>

<%block name="content">
    <h2>${dataset.title}</h2>
    % if request.user.is_admin:
        <h3>Current Schema</h3>
        <form action="/dataset/${dataset.slug}/column/create" method="post">

            <table>
                <tr>
                    <th>Column Name</th>
                    <th>DataType</th>
                    <th>Date Format</th>
                    <th>Remove/Add</th>
                </tr>
                % for field in dataset.fields:
                    <tr>
                        <td>${field.name}</td>
                        <td>${field.data_type}</td>
                        <td>${field.datetime_format}</td>
                        <td>
                            <a href="#">X</a>
                        </td>
                    </tr>
                % endfor

                <tr>
                    <td>
                        <input type="text" name="name" placeholder="Column Name (as appears on CSV)" />
                    </td>

                    <td>
                        <select name="data_type">
                            % for datatype in valid_datatypes:
                                <option value="${datatype}">${datatype}</option>
                            % endfor
                        </select>
                    </td>

                    <td>
                        <input type="text" name="datetime_format" placeholder="Dateformat" />
                    </td>

                    <td>
                        <input type="submit" value="Add Column" />
                    </td>
                </tr>
            </table>

        </form>
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
