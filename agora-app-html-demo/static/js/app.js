document.querySelectorAll('.flash button').forEach((button) => {
  button.addEventListener('click', () => button.parentElement.remove());
});
document.querySelectorAll('form[data-confirm]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});
const sidebarButton = document.querySelector('[data-sidebar]');
if (sidebarButton) sidebarButton.addEventListener('click', () => document.querySelector('#sidebar').classList.toggle('open'));

const classFilter = document.querySelector('[data-filter-class]');
const subjectFilter = document.querySelector('[data-filter-subject]');
const sourcePicker = document.querySelector('[data-source-picker]');
if (classFilter && subjectFilter && sourcePicker) {
  const refreshSources = () => {
    let visible = 0;
    sourcePicker.querySelectorAll('label[data-class]').forEach((item) => {
      const show = item.dataset.class === classFilter.value && item.dataset.subject === subjectFilter.value;
      item.classList.toggle('hidden', !show);
      if (!show) item.querySelector('input').checked = false;
      if (show) visible += 1;
    });
    const empty = sourcePicker.querySelector('[data-source-empty]');
    empty.hidden = visible > 0;
    if (!visible) empty.textContent = classFilter.value && subjectFilter.value
      ? 'Nenhuma fonte aprovada para esta combinação.'
      : 'Selecione turma e disciplina para ver as fontes disponíveis.';
  };
  classFilter.addEventListener('change', refreshSources);
  subjectFilter.addEventListener('change', refreshSources);
  refreshSources();
}

const sourceDrawer = document.querySelector('[data-source-drawer]');
if (sourceDrawer) {
  const setDrawer = (open) => {
    sourceDrawer.classList.toggle('open', open);
    sourceDrawer.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
  };
  document.querySelectorAll('[data-show-sources]').forEach((button) => button.addEventListener('click', () => setDrawer(true)));
  document.querySelectorAll('[data-close-sources]').forEach((button) => button.addEventListener('click', () => setDrawer(false)));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setDrawer(false); });
}
