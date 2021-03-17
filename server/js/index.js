function groupBy(items, key) {
  return items.reduce(
    (result, item) => ({
      ...result,
      [item[key]]: [...(result[item[key]] || []), item],
    }),
    {}
  );
}

async function fetchData() {
  const resp = await fetch(
    `/data/${new Date().toISOString().split("T")[0]}.json`
  );
  if (!resp.ok) {
    throw new Error("Non 200 response from server.");
  }
  return await resp.json();
}

function todayStartTime(hour) {
  const date = new Date();
  date.setHours(hour);
  date.setMinutes(0);
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date;
}

function tomorrowStartTime(hour) {
  const today = todayStartTime(hour);
  today.setDate(today.getDate() + 1);
  return today;
}

function programCell(title, startAt, endAt) {
  const cell = document.createElement("div");
  const titleElem = document.createElement("div");
  const time = document.createElement("div");

  titleElem.classList.add("title");
  time.classList.add("time");

  titleElem.innerText = title;
  time.innerText = formatTime(startAt, endAt);

  cell.appendChild(titleElem);
  cell.appendChild(time);

  return cell;
}

function insertProgramCell(offsetMin, lengthMin, cell) {
  const contents = document.getElementById("contents");
  const row = contents.children.item(offsetMin);
  if (row != null) {
    const td = document.createElement("td");
    td.rowSpan = lengthMin;
    td.appendChild(cell);
    row.appendChild(td);
  }
}

function fillData(data) {
  const container = document.getElementById("container");
  const header = document.getElementById("header");
  const contents = document.getElementById("contents");

  const startTime = todayStartTime(5);

  // Insert <tr></tr> once a minutes for 24 hours
  for (let i = 0; i < 1440; i++) {
    const tr = document.createElement("tr");
    contents.appendChild(tr);
  }

  let prevProgEndTime;

  Object.entries(data).forEach(([station, programs]) => {
    prevProgEndTime = todayStartTime(5);
    const stationName = document.createElement("th");
    stationName.innerText = station;
    header.appendChild(stationName);
    programs.forEach((p) => {
      const startAt = new Date(p.start_at);
      const endAt = new Date(p.end_at);
      const lengthMin = (endAt - startAt) / 1000 / 60;
      const offsetMin = (startAt - startTime) / 1000 / 60;

      insertProgramCell(
        offsetMin,
        lengthMin,
        programCell(p.title, startAt, endAt)
      );

      if (prevProgEndTime < startAt) {
        const offsetMin = (prevProgEndTime - startTime) / 1000 / 60;
        const diffMin = (startAt - prevProgEndTime) / 1000 / 60;
        insertProgramCell(
          offsetMin,
          diffMin,
          programCell("Sleep", prevProgEndTime, startAt)
        );
      }
      prevProgEndTime = endAt;
    });
    const tomorrow = tomorrowStartTime(5);
    if (prevProgEndTime < tomorrow) {
      const offsetMin = (prevProgEndTime - startTime) / 1000 / 60;
      const diffMin = (tomorrow - prevProgEndTime) / 1000 / 60;
      insertProgramCell(
        offsetMin,
        diffMin,
        programCell("Sleep", prevProgEndTime, tomorrow)
      );
    }
  });
}

function formatTime(startAt, endAt) {
  const sH = startAt.getHours().toString().padStart(2, "0");
  const sM = startAt.getMinutes().toString().padStart(2, "0");
  const eH = endAt.getHours().toString().padStart(2, "0");
  const eM = endAt.getMinutes().toString().padStart(2, "0");
  return `${sH}:${sM} - ${eH}:${eM}`;
}

async function main() {
  const programs = await fetchData();
  const grouped = groupBy(programs, "station");
  fillData(grouped);
}

main();
