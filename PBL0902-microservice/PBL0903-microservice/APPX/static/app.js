const services = {
  MS1: {
    read: "/gateway/ms1/cars",
    write: "http://127.0.0.1:5051/cars",
    db: "DB-A",
  },
  MS2: {
    read: "/gateway/ms2/cars",
    write: "http://127.0.0.1:5052/cars",
    db: "DB-A",
  },
  MS3: {
    read: "/gateway/ms3/cars",
    write: "http://127.0.0.1:5053/cars",
    db: "DB-B",
  },
};

const state = {
  service: "MS1",
  cars: [],
  page: 1,
  pageSize: 5,
  query: "",
};

const carsBody = document.querySelector("#carsBody");
const emptyState = document.querySelector("#emptyState");
const tableCount = document.querySelector("#tableCount");
const pageNumber = document.querySelector("#pageNumber");
const prevPage = document.querySelector("#prevPage");
const nextPage = document.querySelector("#nextPage");
const searchInput = document.querySelector("#searchInput");
const addButton = document.querySelector("#addButton");
const carDialog = document.querySelector("#carDialog");
const carForm = document.querySelector("#carForm");
const dialogTitle = document.querySelector("#dialogTitle");
const closeDialog = document.querySelector("#closeDialog");
const cancelButton = document.querySelector("#cancelButton");
const carId = document.querySelector("#carId");
const carOwner = document.querySelector("#carOwner");
const carname = document.querySelector("#carname");
const carbrand = document.querySelector("#carbrand");
const carmodel = document.querySelector("#carmodel");
const carprice = document.querySelector("#carprice");
const description = document.querySelector("#description");
const serviceLabel = document.querySelector("#serviceLabel");
const dbLabel = document.querySelector("#dbLabel");
const serviceTabs = document.querySelectorAll(".service-tab");

function currentPageItems() {
  const start = (state.page - 1) * state.pageSize;
  return state.cars.slice(start, start + state.pageSize);
}

function serviceGroup(service) {
  return service === "MS3" ? "site-b" : "site-a";
}

function ownerOf(car) {
  return (car.service || car.source_service || state.service).toUpperCase();
}

function sortForCurrentService(cars) {
  const activeGroup = serviceGroup(state.service);
  return [...cars].sort((left, right) => {
    const leftOwner = ownerOf(left);
    const rightOwner = ownerOf(right);
    const leftPriority = serviceGroup(leftOwner) === activeGroup ? 0 : 1;
    const rightPriority = serviceGroup(rightOwner) === activeGroup ? 0 : 1;
    return leftPriority - rightPriority || left.id - right.id;
  });
}

function renderCars() {
  const pageCount = Math.max(1, Math.ceil(state.cars.length / state.pageSize));
  if (state.page > pageCount) state.page = pageCount;

  serviceLabel.textContent = `Microservice ${state.service}`;
  dbLabel.textContent = services[state.service].db;

  serviceTabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.service === state.service);
  });

  carsBody.innerHTML = "";
  currentPageItems().forEach((car) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>#${car.id}</td>
      <td><span class="brand-pill"></span></td>
      <td class="car-name"></td>
      <td></td>
      <td></td>
      <td class="price"></td>
      <td class="description"></td>
      <td class="actions">
        <button class="action-button edit-button" type="button">Edit</button>
        <button class="action-button delete-button" type="button">Del</button>
      </td>
    `;

    tr.querySelector(".brand-pill").textContent = ownerOf(car);
    tr.children[2].textContent = car.carname;
    tr.children[3].textContent = car.carbrand;
    tr.children[4].textContent = car.carmodel;
    tr.children[5].textContent = car.carprice;
    tr.children[6].textContent = car.description || "-";
    tr.querySelector(".edit-button").addEventListener("click", () => openEditDialog(car));
    tr.querySelector(".delete-button").addEventListener("click", () => deleteCar(car));
    carsBody.appendChild(tr);
  });

  emptyState.hidden = state.cars.length !== 0;
  tableCount.innerHTML = `Menampilkan <strong>${state.cars.length}</strong> mobil dari ${services[state.service].db}`;
  pageNumber.textContent = String(state.page);
  prevPage.disabled = state.page <= 1;
  nextPage.disabled = state.page >= pageCount;
}

async function loadCars() {
  const params = new URLSearchParams();
  if (state.query) params.set("q", state.query);

  const response = await fetch(`${services[state.service].read}?${params.toString()}`);
  if (!response.ok) throw new Error("Gagal mengambil data mobil");

  state.cars = sortForCurrentService(await response.json());
  renderCars();
}

function openCreateDialog() {
  dialogTitle.textContent = `Tambah Mobil ${state.service}`;
  carId.value = "";
  carOwner.value = "";
  carForm.reset();
  description.value = `input from APPX to ${state.service}`;
  carDialog.showModal();
  carname.focus();
}

function openEditDialog(car) {
  const owner = ownerOf(car);
  dialogTitle.textContent = `Edit Mobil ${owner}`;
  carId.value = car.id;
  carOwner.value = owner;
  carname.value = car.carname;
  carbrand.value = car.carbrand;
  carmodel.value = car.carmodel;
  carprice.value = car.carprice;
  description.value = car.description || "";
  carDialog.showModal();
  carname.focus();
}

function closeCarDialog() {
  carDialog.close();
}

async function saveCar(event) {
  event.preventDefault();

  const payload = {
    carname: carname.value.trim(),
    carbrand: carbrand.value.trim(),
    carmodel: carmodel.value.trim(),
    carprice: carprice.value.trim(),
    description: description.value.trim(),
  };

  const id = carId.value;
  const owner = carOwner.value || state.service;
  const ownerParam = id ? `?owner=${encodeURIComponent(owner)}` : "";
  const response = await fetch(id ? `${services[state.service].write}/${id}${ownerParam}` : services[state.service].write, {
    method: id ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    alert("Data mobil gagal disimpan.");
    return;
  }

  closeCarDialog();
  await loadCars();
}

async function deleteCar(car) {
  const owner = ownerOf(car);
  if (!confirm(`Hapus ${car.carname} dari ${owner}?`)) return;

  const response = await fetch(`${services[state.service].write}/${car.id}?owner=${encodeURIComponent(owner)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    alert("Data mobil gagal dihapus.");
    return;
  }

  await loadCars();
}

let searchTimer;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    state.query = searchInput.value.trim();
    state.page = 1;
    await loadCars();
  }, 250);
});

serviceTabs.forEach((tab) => {
  tab.addEventListener("click", async () => {
    state.service = tab.dataset.service;
    state.page = 1;
    await loadCars();
  });
});

addButton.addEventListener("click", openCreateDialog);
closeDialog.addEventListener("click", closeCarDialog);
cancelButton.addEventListener("click", closeCarDialog);
carForm.addEventListener("submit", saveCar);

prevPage.addEventListener("click", () => {
  state.page -= 1;
  renderCars();
});

nextPage.addEventListener("click", () => {
  state.page += 1;
  renderCars();
});

loadCars().catch(() => {
  emptyState.hidden = false;
  emptyState.textContent = "Data mobil gagal dimuat. Pastikan APPX, MS1, MS2, dan MS3 berjalan.";
});
