document.addEventListener("DOMContentLoaded", async function () {
  const content = document.querySelector(".content");
  const token = localStorage.getItem("access_token");
  const searchInput = document.querySelector('input[type="search"]');
  const searchButton = document.querySelector(".search button");

  if (!token) {
    alert("Sessão expirada! Faça login novamente.");
    window.location.href = "/api/usuarios/";
    return;
  }

  //Função que renderiza as vagas
  async function carregarVagas() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/vagas/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

      const data = await response.json();

      content.innerHTML = "<h1>Vagas criadas por você</h1>";

      if (data.results?.length) {
        data.results.forEach((vaga) => {
          const vagaHTML = `
            <div class="box-vaga">
              <div class="vaga">
                <p><strong>${vaga.id}</strong></p>
                <p><strong>${vaga.nome_cargo}</strong></p>
                <p><strong>Data:</strong> ${new Date(vaga.data_solicitacao).toLocaleDateString()}</p>
              </div>

              <div class="box-descricao">
                <div class="box-descricao-text">
                  <hr />
                  <p class="status-andamento-ab">${vaga.status}</p>
                  <div><strong>Número de vagas:</strong> ${vaga.quantidade}</div>
                  <div><strong>Tipo de contrato:</strong> ${vaga.tipo_contrato}</div>
                  <div><strong>Modalidade:</strong> ${vaga.modalidade}</div>
                  <div><strong>Prioridade:</strong> ${vaga.prioridade}</div>
                  <div><strong>Observações:</strong> ${vaga.observacao || "Nenhuma"}</div>
                </div>
              </div>
              <div class="resultado">
                <button class="resultados-btn">Resultados</button>
              </div>
            </div>
          `;
          content.insertAdjacentHTML("beforeend", vagaHTML);
        });
      } else {
        content.innerHTML += "<p>Nenhuma vaga encontrada :(</p>";
      }
    } catch (error) {
      console.error("Erro ao carregar vagas:", error);
      alert("Erro ao carregar as vagas. Tente novamente mais tarde.");
    }
  }

  //Chama o carregamento inicial
  await carregarVagas();

  //Função de busca
  function realizarBusca(termo) {
    const termoLimpo = termo.trim().toLowerCase();
    const vagas = content.querySelectorAll(".vaga");
    let encontrouAlguma = false;

    vagas.forEach((vaga) => {
      const texto = vaga.innerText.toLowerCase();
      const box = vaga.closest(".box-vaga");
      if (texto.includes(termoLimpo) || termoLimpo === "") {
        box.style.display = "block";
        encontrouAlguma = true;
      } else {
        box.style.display = "none";
      }
    });

    // Se não encontrar nada
    let msg = content.querySelector(".mensagem-nenhuma-vaga");
    if (!msg) {
      msg = document.createElement("p");
      msg.classList.add("mensagem-nenhuma-vaga");
      msg.style.color = "#fff";
      msg.style.fontStyle = "italic";
      msg.textContent = "Nenhuma vaga encontrada :(";
      content.appendChild(msg);
    }
    msg.style.display = encontrouAlguma ? "none" : "block";
  }

  // Evento de busca
  searchButton.addEventListener("click", (e) => {
    e.preventDefault();
    realizarBusca(searchInput.value);
  });
  searchInput.addEventListener("input", () => realizarBusca(searchInput.value));
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      realizarBusca(searchInput.value);
    }
  });

  // Delegação de eventos (abrir/fechar descrição e botão de resultados)
  content.addEventListener("click", (e) => {
    // Clique no botão de resultados
    if (e.target.classList.contains("resultados-btn")) {
      const vagaBox = e.target.closest(".box-vaga");
      const vagaId = vagaBox.querySelector(".vaga p strong").innerText; 
      window.location.href = `/candidatos/resultado/${vagaId}/`;
      return; // Evita executar o toggle
    }

    // Clique na vaga para abrir/fechar box de descrição
    const vaga = e.target.closest(".vaga");
    if (!vaga) return;

    const descricao = vaga.nextElementSibling;
    const resultado = descricao?.nextElementSibling;

    vaga.classList.toggle("aberta");
    descricao?.classList.toggle("aberta");
    resultado?.classList.toggle("visivel");
  });
});
