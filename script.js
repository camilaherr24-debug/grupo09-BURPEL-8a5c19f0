console.log("✅ Proyecto cargado correctamente");

// Dirección de tu servidor
const API_URL = "http://127.0.0.1:5000/api";

// Saber en qué página estamos
const paginaActual = window.location.pathname;

// ------------------------------
// PÁGINA DE TECNOLOGÍAS
// ------------------------------
if (paginaActual.includes("tecnologias.html")) {
  cargarTecnologias();
  
  const buscador = document.getElementById("filtro-tecnologia");
  if (buscador) {
    buscador.addEventListener("input", (e) => filtrarLista(e.target.value, ".tarjeta-tecnologia"));
  }
}

// ------------------------------
// PÁGINA DE LENGUAJES
// ------------------------------
if (paginaActual.includes("lenguajes.html")) {
  cargarLenguajes();
  
  const buscador = document.getElementById("filtro-lenguaje");
  if (buscador) {
    buscador.addEventListener("input", (e) => filtrarLista(e.target.value, ".tarjeta-lenguaje"));
  }
}

// ------------------------------
// TRAER TECNOLOGÍAS DESDE EL SERVIDOR
// ------------------------------
async function cargarTecnologias() {
  const contenedor = document.getElementById("lista-tecnologias");
  
  try {
    const respuesta = await fetch(`${API_URL}/tecnologias`);
    
    if (!respuesta.ok) throw new Error("No se pudo conectar");
    
    const datos = await respuesta.json();
    mostrarTecnologias(datos, contenedor);
    
  } catch (error) {
    contenedor.innerHTML = `<p class="cargando">Error al cargar: ${error.message}</p>`;
    console.error("🔴 Error:", error);
  }
}

// ------------------------------
// TRAER LENGUAJES DESDE EL SERVIDOR
// ------------------------------
async function cargarLenguajes() {
  const contenedor = document.getElementById("lista-lenguajes");
  
  try {
    const respuesta = await fetch(`${API_URL}/lenguajes`);
    
    if (!respuesta.ok) throw new Error("No se pudo conectar");
    
    const datos = await respuesta.json();
    mostrarLenguajes(datos, contenedor);
    
  } catch (error) {
    contenedor.innerHTML = `<p class="cargando">Error al cargar: ${error.message}</p>`;
    console.error("🔴 Error:", error);
  }
}

// ------------------------------
// ARMAR TARJETAS DE TECNOLOGÍAS
// ------------------------------
function mostrarTecnologias(lista, contenedor) {
  contenedor.innerHTML = "";
  
  lista.forEach(item => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "tarjeta tarjeta-tecnologia";
    tarjeta.innerHTML = `
      <h3>${item.nombre}</h3>
      <p><strong>Tipo:</strong> ${item.tipo || "No especificado"}</p>
      <p><strong>Descripción:</strong> ${item.descripcion || "Sin descripción"}</p>
    `;
    contenedor.appendChild(tarjeta);
  });
}

// ------------------------------
// ARMAR TARJETAS DE LENGUAJES
// ------------------------------
function mostrarLenguajes(lista, contenedor) {
  contenedor.innerHTML = "";
  
  lista.forEach(item => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "tarjeta tarjeta-lenguaje";
    tarjeta.innerHTML = `
      <h3>${item.nombre}</h3>
      <p><strong>Año de creación:</strong> ${item.anio || "Desconocido"}</p>
      <p><strong>Paradigma:</strong> ${item.paradigma || "No especificado"}</p>
    `;
    contenedor.appendChild(tarjeta);
  });
}

// ------------------------------
// BUSCADOR / FILTRO
// ------------------------------
function filtrarLista(texto, claseTarjeta) {
  const tarjetas = document.querySelectorAll(`.${claseTarjeta}`);
  tarjetas.forEach(tarjeta => {
    const textoTarjeta = tarjeta.textContent.toLowerCase();
    if (textoTarjeta.includes(texto.toLowerCase())) {
      tarjeta.style.display = "block";
    } else {
      tarjeta.style.display = "none";
    }
  });