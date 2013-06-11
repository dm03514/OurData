<%inherit file="ourdata:templates/base.mak" />

<%block name="title">User Permissions Edit</%block>

<%block name="navigation"></%block>

<%block name="content">
    <form action="${request.route_url('add_credentials', user_id=user_id)}" method="post">
    </form>
</%block>
