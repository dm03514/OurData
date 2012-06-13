<%inherit file="ourdata:templates/base.mak" />

<%block name="title">Logged In</%block>

<%block name="navigation"></%block>

<%block name="content">
    % if credentials:
        % for credential in credentials:
            ${credential}
        % endfor
    % endif
</%block>

<%block name="sidebar">
    <h3>Links</h3>
    <ul>
        <li></li>
        <li></li>
    </ul>
</%block>
