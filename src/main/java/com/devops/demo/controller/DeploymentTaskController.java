package com.devops.demo.controller;

import com.devops.demo.model.DeploymentTask;
import com.devops.demo.repository.DeploymentTaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/v1/tasks")
@CrossOrigin(origins = "*")
public class DeploymentTaskController {

    private final DeploymentTaskRepository taskRepository;

    @Autowired
    public DeploymentTaskController(DeploymentTaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    // 1. GET ALL
    @GetMapping
    public ResponseEntity<List<DeploymentTask>> getAllTasks() {
        return ResponseEntity.ok(taskRepository.findAllByOrderByCreatedAtDesc());
    }

    // 2. GET BY ID
    @GetMapping("/{id}")
    public ResponseEntity<DeploymentTask> getTaskById(@PathVariable Long id) {
        return taskRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // 3. CREATE (POST)
    @PostMapping
    public ResponseEntity<DeploymentTask> createTask(@RequestBody DeploymentTask task) {
        if (task.getStatus() == null || task.getStatus().isBlank()) {
            task.setStatus("PENDING");
        }
        if (task.getDeployedBy() == null || task.getDeployedBy().isBlank()) {
            task.setDeployedBy("Cloud Run DevOps User");
        }
        DeploymentTask saved = taskRepository.save(task);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    // 4. UPDATE (PUT)
    @PutMapping("/{id}")
    public ResponseEntity<DeploymentTask> updateTask(@PathVariable Long id, @RequestBody DeploymentTask updatedTask) {
        return taskRepository.findById(id)
                .map(existing -> {
                    if (updatedTask.getServiceName() != null) existing.setServiceName(updatedTask.getServiceName());
                    if (updatedTask.getVersion() != null) existing.setVersion(updatedTask.getVersion());
                    if (updatedTask.getEnvironment() != null) existing.setEnvironment(updatedTask.getEnvironment());
                    if (updatedTask.getStatus() != null) existing.setStatus(updatedTask.getStatus());
                    if (updatedTask.getDeployedBy() != null) existing.setDeployedBy(updatedTask.getDeployedBy());
                    DeploymentTask saved = taskRepository.save(existing);
                    return ResponseEntity.ok(saved);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // 5. DELETE
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, Object>> deleteTask(@PathVariable Long id) {
        Optional<DeploymentTask> task = taskRepository.findById(id);
        if (task.isPresent()) {
            taskRepository.deleteById(id);
            Map<String, Object> response = new HashMap<>();
            response.put("deleted", true);
            response.put("id", id);
            response.put("message", "Task deleted successfully");
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // 6. METRICS & STATS
    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getStats() {
        List<DeploymentTask> all = taskRepository.findAll();
        long total = all.size();
        long deployed = all.stream().filter(t -> "DEPLOYED".equalsIgnoreCase(t.getStatus())).count();
        long inProgress = all.stream().filter(t -> "IN_PROGRESS".equalsIgnoreCase(t.getStatus())).count();
        long failed = all.stream().filter(t -> "FAILED".equalsIgnoreCase(t.getStatus())).count();
        long pending = all.stream().filter(t -> "PENDING".equalsIgnoreCase(t.getStatus())).count();

        Map<String, Object> stats = new HashMap<>();
        stats.put("total", total);
        stats.put("deployed", deployed);
        stats.put("inProgress", inProgress);
        stats.put("failed", failed);
        stats.put("pending", pending);
        return ResponseEntity.ok(stats);
    }
}
