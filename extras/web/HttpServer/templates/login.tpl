{% include 'header.tpl' %}
{% if errMsg %}
<div class="errMsg"> {{ errMsg }} </div>
{% endif %}
<div class="auth">
<form action="/login" method="POST">
<table>
<tr>
<td><label>Username</label></td>
<td><input type="text" width="30" name="user" /></td>
</tr>
<tr>
<td><label>Password</label></td>
<td><input type="password" width="30" name="passwd" /></td>
</table>
<input type="submit" width="30" name="ok" value="Login" />
</form>
</div>
{% include 'footer.tpl' %}
