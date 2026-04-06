import { useState } from 'react';
import './TaskForm.css';

const departments = [
  { value: 'finance', label: 'Финансы' },
  { value: 'hr', label: 'HR' },
  { value: 'it', label: 'IT' },
  { value: 'marketing', label: 'Маркетинг' },
  { value: 'operations', label: 'Операции' }
];

function TaskForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    department: 'it'
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.title.trim()) {
      setError('Название задачи обязательно');
      return;
    }

    if (!formData.description.trim()) {
      setError('Описание задачи обязательно');
      return;
    }

    setSubmitting(true);
    try {
      await onSubmit(formData);
      setFormData({
        title: '',
        description: '',
        department: 'it'
      });
    } catch (err) {
      setError('Ошибка при создании задачи');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <h2>Новая задача</h2>
      
      {error && <div className="form-error">{error}</div>}
      
      <div className="form-group">
        <label htmlFor="title">Название задачи *</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Введите название задачи"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Описание *</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Подробное описание задачи"
          rows="4"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="department">Отдел</label>
        <select
          id="department"
          name="department"
          value={formData.department}
          onChange={handleChange}
        >
          {departments.map(dept => (
            <option key={dept.value} value={dept.value}>
              {dept.label}
            </option>
          ))}
        </select>
      </div>

      <div className="form-hint">
        <p>💡 После создания задачи вы сможете загрузить фотографии для отчета</p>
      </div>

      <button 
        type="submit" 
        className="submit-btn"
        disabled={submitting}
      >
        {submitting ? 'Создание...' : 'Создать задачу'}
      </button>
    </form>
  );
}

export default TaskForm;
