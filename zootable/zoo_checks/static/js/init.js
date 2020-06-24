document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".sidenav");
  var instances = M.Sidenav.init(elems, {});
});

document.querySelectorAll("input[type=radio]").forEach((elem) => {
  elem.addEventListener("click", allowUncheck);
  // only needed if elem can be pre-checked
  elem.previous = elem.checked;
});

function allowUncheck(e) {
  if (this.previous) {
    this.checked = false;
  }
  // need to update previous on all elements of this group
  // (either that or store the id of the checked element)
  document
    .querySelectorAll(`input[type=radio][name=${this.name}]`)
    .forEach((elem) => {
      elem.previous = elem.checked;
    });
}

function change_tally_form() {
  const tally_date = document.getElementById("id_tally_date").value;
  if (tally_date != "") {
    document.getElementById("datepicker_form").submit();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".datepicker");
  var today = new Date();
  var instances = M.Datepicker.init(elems, {
    format: "mm/dd/yyyy",
    maxDate: today,
    autoClose: true,
  });
});

// this overwrites the init for all datepicker's above
document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll("#id_tally_date");
  var today = new Date();
  var instances = M.Datepicker.init(elems, {
    format: "mm/dd/yyyy",
    maxDate: today,
    autoClose: false,
    onClose: function () {
      change_tally_form();
    },
  });
});

function incrementValue(id, inc_val) {
  var value = parseInt(document.getElementById(id).value, 10);
  value = isNaN(value) ? 0 : value;
  if (value + inc_val >= 0) {
    value += inc_val;
    document.getElementById(id).value = value;
  }
}

function chartVisible(id) {
  document.getElementById(id).style.display = "block";
  document.getElementById(id + "-btn").classList.add("disabled");

  const elems = ["line-chart-opt", "pie-chart-opt"];
  let index = elems.indexOf(id);
  if (index > -1) {
    elems.splice(index, 1);
  }

  elems.forEach((item, index) => {
    document.getElementById(item).style.display = "none";
    document.getElementById(item + "-btn").classList.remove("disabled");
  });
}

document
  .querySelectorAll(".condition-radio input[type=radio]")
  .forEach((elem) => {
    elem.addEventListener("click", function (e) {
      // needs attention causes comment field to appear
      let comment_field =
        elem.parentElement.parentElement.parentElement.nextElementSibling;
      if (elem.value === "NA" || elem.value === "AB") {
        comment_field.style.display = "block";
      }
    });
  });

function update_count_bar(slider_elem) {
  const count_bar_id = slider_elem.id.replace("_slider", "");
  document.getElementById(count_bar_id).value = slider_elem.value;
}

function update_count_seen(slider_elem) {
  // const total = slider_elem.max;
  const count_seen_id = slider_elem.id.replace("_slider", "");
  document.getElementById(count_seen_id).value = slider_elem.value;

  update_bar_elems(
    slider_elem.id.replace("_seen_slider", "_bar_slider"),
    slider_elem.value
  );
}

function update_bar_elems(count_bar_id, seen_value) {
  //set the slider max value for BAR
  const count_bar = document.getElementById(count_bar_id);
  if (parseInt(seen_value) < parseInt(count_bar.value)) {
    // set the count_bar value to max of seen and BAR
    count_bar.value = seen_value;
    update_count_bar(count_bar);
  }
  count_bar.max = seen_value;
}

function update_slider(slider_id, value) {
  document.getElementById(slider_id).value = value;
}

document.querySelectorAll(".count_seen_slider").forEach((elem) => {
  elem.addEventListener("input", function (e) {
    update_count_seen(elem);
  });
});

document.querySelectorAll(".count_bar_slider").forEach((elem) => {
  elem.addEventListener("input", function (e) {
    update_count_bar(elem);
  });
});

document
  .querySelectorAll(".count_seen_input,.count_bar_input")
  .forEach((elem) => {
    elem.addEventListener("input", function (e) {
      update_slider(elem.id + "_slider", elem.value);
      if (elem.className.includes("count_seen_input")) {
        update_bar_elems(
          elem.id.replace("_seen", "_bar") + "_slider",
          elem.value
        );
      }
    });
  });

document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".tooltipped");
  var instances = M.Tooltip.init(elems, {});
});

function update_species_count_elem(species_form_id, counted) {
  const q_sel = "td#" + species_form_id + " p input";
  const species_input = document.querySelector(q_sel);

  if (parseInt(species_input.value) < counted) {
    species_input.value = counted.toString();
  }
}

function count_species_animals_conditions(condition_radio_td_id) {
  const radio_selector =
    "td#" + condition_radio_td_id + " .condition-radio input[type=radio]";
  let cond_counted = 0;
  document.querySelectorAll(radio_selector).forEach((elem) => {
    if (elem.checked && elem.value != "NS") {
      cond_counted += 1;
    }
  });
  return cond_counted;
}

document
  .querySelectorAll(".tally-table-body .condition-radio input[type=radio]")
  .forEach((elem) => {
    elem.addEventListener("click", function (e) {
      const condition_radio_td_id =
        elem.parentElement.parentElement.parentElement.parentElement.id;

      cond_counted = count_species_animals_conditions(condition_radio_td_id);

      const species_form_id = condition_radio_td_id.replace(
        "_animal_condition_form",
        "_form"
      );
      update_species_count_elem(species_form_id, cond_counted);
    });
  });

document.querySelectorAll(".msg").forEach((elem) => {
  elem.addEventListener("animationend", () => {
    elem.style.display = "none";
  });
});
