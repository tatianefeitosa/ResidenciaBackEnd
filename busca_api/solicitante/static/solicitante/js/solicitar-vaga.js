document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // --- Campos simples ---
    const nome_cargo = document.getElementById("nome-cargo").value.trim();
    const quantidade = parseInt(document.getElementById("num-vagas").value);
    const prioridade = document.getElementById("prioridade-vaga").value;
    const observacao = document.getElementById("observacao").value.trim();

    // --- Campos diretos ---
    const modalidade = document.getElementById("modalidade-trabalho").value;
    const tipo_contrato = "Prazo indeterminado"; // se tiver campo específico, substitua

    // --- Habilidades Técnicas ---
    const habilidadesTecnicas = Array.from(
      document.querySelectorAll("#container-habilidades-tecnicas input")
    ).map(input => ({ nome: input.value.trim() }))
     .filter(obj => obj.nome !== "");

    // --- Habilidades Interpessoais ---
    const habilidadesInterpessoais = Array.from(
      document.querySelectorAll("#container-habilidades-inter input")
    ).map(input => ({ nome: input.value.trim() }))
     .filter(obj => obj.nome !== "");

    // --- Diplomas ---
    const diplomaTipo = document.getElementById("diploma").value;
    const area = document.getElementById("area-estudo").value.trim();
    const diplomas = diplomaTipo ? [{ tipo: diplomaTipo, area }] : [];

    // --- Certificações ---
    const certificacaoNome = document.getElementById("certificacao").value.trim();
    const certificacoes = certificacaoNome ? [{ nome: certificacaoNome }] : [];

    // --- Idiomas ---
    const idiomaNome = document.getElementById("idiomas").value.trim();
    const idiomaNivel = document.getElementById("nivel-idioma").value;
    const idiomas = idiomaNome ? [{ nome: idiomaNome, nivel: idiomaNivel }] : [];

    // --- Experiência ---
    const empresaNome = document.getElementById("empresas").value.trim();
    const empresaNivel = document.getElementById("nivel-experiencia").value;
    const empresas = empresaNome ? [{ nome: empresaNome, nivel: empresaNivel }] : [];

    // --- Localização ---
    const pais = document.getElementById("pais").value.trim();
    const estado = document.getElementById("estado").value.trim();
    const cidade = document.getElementById("cidade").value.trim();
    const localizacoes = pais || estado || cidade ? [{ pais, estado, cidade }] : [];

    // --- Montar objeto final ---
    const vagaData = {
      nome_cargo,
      modalidade,
      tipo_contrato,
      quantidade,
      prioridade,
      observacao,
      habilidades_tecnicas: habilidadesTecnicas,
      habilidades_interpessoais: habilidadesInterpessoais,
      diplomas,
      certificacoes,
      idiomas,
      empresas,
      localizacoes,
      status: "Pendente",
    };

    console.log("Dados enviados:", vagaData);

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch("http://127.0.0.1:8000/api/vagas/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(vagaData),
      });

      if (!response.ok) {
        const error = await response.json();
        console.error("Erro ao criar vaga:", error);
        alert("Erro ao criar vaga. Verifique os campos e tente novamente.");
        return;
      }

      alert("Vaga criada com sucesso!");
      form.reset();

      const tipoUsuario = localStorage.getItem("tipo_usuario");

        if (tipoUsuario === "administracao") {
          window.location.href = "/administracao/";
        } else {
          window.location.href = "/solicitante/";
        }

    } catch (err) {
      console.error("Erro na requisição:", err);
      alert("Erro de conexão com o servidor.");
    }
  });
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
