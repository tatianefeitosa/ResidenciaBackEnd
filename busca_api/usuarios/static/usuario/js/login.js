document.addEventListener("DOMContentLoaded", function () {
  const botaoEntrar = document.getElementById("botao-entrar");

  botaoEntrar.addEventListener("click", async function () {
    const usuario = document.getElementById("usuario-input").value;
    const senha = document.getElementById("password-input").value;
    const tipoUsuario = document.getElementById("tipo-usuario").value;

    if (!usuario || !senha) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/usuarios/login/", {//
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: usuario, // ou "username", dependendo do que seu serializer espera
          password: senha,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Login bem-sucedido:", data);
        alert("Login realizado com sucesso!");
        // Exemplo: redirecionar para a página do tipo de usuário
        if (tipoUsuario === "administracao") {
          window.location.href = "/administracao/";
        } else {
          window.location.href = "/solicitante/";
        }
      } else {
        alert(data.detail || "Usuário ou senha incorretos.");
      }
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      alert("Erro de conexão com o servidor.");
    }
  });
});