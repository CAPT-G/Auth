<div id="signupModal" class="modal" {% if show_modal == "signup" %}style="display:block;"{% endif %}>
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('signupModal').style.display='none'">&times;</span>
    <h2>Sign Up</h2>
    {% if signup_error %}<p style="color:red;">{{ signup_error }}</p>{% endif %}
    <form method="post" action="{% url 'accounts:signup' %}">
      {% csrf_token %}
      {{ signup_form.as_p }}
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="#" id="switchToLogin">Log In</a></p>
  </div>
</div>

<div id="loginModal" class="modal" {% if show_modal == "login" %}style="display:block;"{% endif %}>
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('loginModal').style.display='none'">&times;</span>
    <h2>Log In</h2>
    {% if login_error %}<p style="color:red;">{{ login_error }}</p>{% endif %}
    <form method="post" action="{% url 'accounts:login' %}">
      {% csrf_token %}
      {{ login_form.as_p }}
      <button type="submit">Log In</button>
    </form>
    <p>Don't have an account? <a href="#" id="switchToSignup">Sign Up</a></p>
  </div>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function() {
    const loginLink = document.getElementById("switchToLogin");
    const signupLink = document.getElementById("switchToSignup");
    if (loginLink) {
      loginLink.addEventListener("click", function(e) {
        e.preventDefault();
        document.getElementById("signupModal").style.display = "none";
        document.getElementById("loginModal").style.display = "block";
      });
    }
    if (signupLink) {
      signupLink.addEventListener("click", function(e) {
        e.preventDefault();
        document.getElementById("loginModal").style.display = "none";
        document.getElementById("signupModal").style.display = "block";
      });
    }
  });
</script>
