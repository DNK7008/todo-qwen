import { useState } from 'react';
import './PhotoGallery.css';

function PhotoGallery({ tasks, user }) {
  const [selectedTask, setSelectedTask] = useState(null);
  const [filterDepartment, setFilterDepartment] = useState('all');

  const filteredTasks = filterDepartment === 'all'
    ? tasks
    : tasks.filter(task => task.department === filterDepartment);

  const allPhotos = filteredTasks
    .filter(task => task.photos && task.photos.length > 0)
    .flatMap(task => 
      task.photos.map((photo, index) => ({
        photo,
        taskId: task.id,
        taskTitle: task.title,
        department: task.department
      }))
    );

  const departments = ['all', ...new Set(tasks.map(t => t.department))];

  return (
    <div className="photo-gallery">
      <div className="gallery-header">
        <h2>Фотогалерея</h2>
        <select
          value={filterDepartment}
          onChange={(e) => setFilterDepartment(e.target.value)}
          className="department-filter"
        >
          <option value="all">Все отделы</option>
          <option value="finance">Финансы</option>
          <option value="hr">HR</option>
          <option value="it">IT</option>
          <option value="marketing">Маркетинг</option>
          <option value="operations">Операции</option>
        </select>
      </div>

      {user && (
        <div className="user-folder-info">
          <p>📁 Ваша папка: <strong>/users/{user.id}/photos</strong></p>
          <p className="hint">Загруженные фото автоматически сохраняются в вашу персональную папку</p>
        </div>
      )}

      {allPhotos.length === 0 ? (
        <div className="gallery-empty">
          <p>Нет фотографий для отображения</p>
          <p className="hint">Загрузите фото к задачам, чтобы они появились здесь</p>
        </div>
      ) : (
        <>
          <div className="photo-grid">
            {allPhotos.map((item, index) => (
              <div 
                key={`${item.taskId}-${index}`} 
                className="photo-item"
                onClick={() => setSelectedTask(item)}
              >
                <img 
                  src={`/placeholder-${index}.jpg`} 
                  alt={item.taskTitle}
                />
                <div className="photo-overlay">
                  <span className="photo-task-title">{item.taskTitle}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="gallery-stats">
            <p>Всего фото: <strong>{allPhotos.length}</strong></p>
          </div>
        </>
      )}

      {selectedTask && (
        <div className="modal-overlay" onClick={() => setSelectedTask(null)}>
          <div className="modal-content photo-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedTask.taskTitle}</h3>
              <button 
                className="close-btn"
                onClick={() => setSelectedTask(null)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-photo-large">
              <img 
                src={`/placeholder-0.jpg`} 
                alt={selectedTask.taskTitle}
              />
            </div>
            
            <div className="modal-photo-info">
              <p><strong>Задача:</strong> {selectedTask.taskTitle}</p>
              <p><strong>Отдел:</strong> {selectedTask.department}</p>
              <p><strong>Путь на сервере:</strong> /users/{user?.id || 'xxx'}/photos/task_{selectedTask.taskId}/</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default PhotoGallery;
