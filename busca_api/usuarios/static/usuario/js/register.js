document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register-form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("senha").value.trim();
    const tipo = document.getElementById("tipo").value;
    const setor = document.getElementById("setor").value.trim();
    const cargo = document.getElementById("cargo").value.trim();

    if (!nome || !email || !senha || !tipo || !setor || !cargo) {
      alert("Preencha todos os campos!");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/usuarios/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nome,
          email,
          password,
          tipo,
          setor,
          cargo,
        }),
      });

      if (response.ok) {
        alert("Usuário registrado com sucesso!");
        if (tipo === "administracao") {
          window.location.href = "/admin/dashboard/";
        } else {
          window.location.href = "/solicitante/";
        }
          } else {
        const data = await response.json();
        alert(`Erro ao registrar: ${data.detail || "Verifique os dados."}`);
      }
    } catch (error) {
      alert("Erro na conexão com o servidor.");
      console.error(error);
    }
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
