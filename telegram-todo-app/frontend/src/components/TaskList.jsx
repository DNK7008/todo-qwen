import { useState } from 'react';
import './TaskList.css';

const statusLabels = {
  pending: 'Ожидает',
  in_progress: 'В работе',
  completed: 'Завершено'
};

const statusColors = {
  pending: '#ffc107',
  in_progress: '#2196f3',
  completed: '#4caf50'
};

const departmentLabels = {
  finance: 'Финансы',
  hr: 'HR',
  it: 'IT',
  marketing: 'Маркетинг',
  operations: 'Операции'
};

function TaskList({ tasks, onUpdateStatus, onUploadPhotos }) {
  const [selectedTask, setSelectedTask] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileSelect = async (taskId, event) => {
    const files = Array.from(event.target.files);
    if (files.length === 0) return;

    setUploading(true);
    try {
      await onUploadPhotos(taskId, files);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handleStatusChange = (taskId, newStatus) => {
    onUpdateStatus(taskId, newStatus);
  };

  if (tasks.length === 0) {
    return (
      <div className="task-list-empty">
        <p>Нет задач. Создайте новую задачу!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map(task => (
        <div key={task.id} className="task-card">
          <div className="task-header">
            <h3 className="task-title">{task.title}</h3>
            <span 
              className="task-status"
              style={{ backgroundColor: statusColors[task.status] }}
            >
              {statusLabels[task.status]}
            </span>
          </div>
          
          <p className="task-description">{task.description}</p>
          
          <div className="task-meta">
            <span className="task-department">
              {departmentLabels[task.department] || task.department}
            </span>
            <span className="task-date">
              {new Date(task.createdAt).toLocaleDateString('ru-RU')}
            </span>
          </div>

          {task.photos && task.photos.length > 0 && (
            <div className="task-photos-preview">
              <span className="photos-count">📷 {task.photos.length} фото</span>
              <div className="photo-thumbnails">
                {task.photos.slice(0, 3).map((photo, index) => (
                  <div key={index} className="thumbnail">
                    <img src={`/placeholder-${index}.jpg`} alt={`Photo ${index + 1}`} />
                  </div>
                ))}
                {task.photos.length > 3 && (
                  <div className="thumbnail more">
                    <span>+{task.photos.length - 3}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="task-actions">
            <select
              value={task.status}
              onChange={(e) => handleStatusChange(task.id, e.target.value)}
              className="status-select"
            >
              <option value="pending">Ожидает</option>
              <option value="in_progress">В работе</option>
              <option value="completed">Завершено</option>
            </select>

            <label className="upload-btn">
              <input
                type="file"
                accept="image/*"
                multiple
                onChange={(e) => handleFileSelect(task.id, e)}
                disabled={uploading}
              />
              {uploading ? 'Загрузка...' : '📷 Добавить фото'}
            </label>

            <button 
              className="view-gallery-btn"
              onClick={() => setSelectedTask(task)}
            >
              Просмотр галереи
            </button>
          </div>
        </div>
      ))}

      {selectedTask && (
        <div className="modal-overlay" onClick={() => setSelectedTask(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h2>{selectedTask.title}</h2>
            <div className="modal-gallery">
              {selectedTask.photos && selectedTask.photos.length > 0 ? (
                selectedTask.photos.map((photo, index) => (
                  <div key={index} className="modal-photo">
                    <img src={`/placeholder-${index}.jpg`} alt={`Photo ${index + 1}`} />
                  </div>
                ))
              ) : (
                <p>Нет фотографий для этой задачи</p>
              )}
            </div>
            <button 
              className="close-btn"
              onClick={() => setSelectedTask(null)}
            >
              Закрыть
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default TaskList;
