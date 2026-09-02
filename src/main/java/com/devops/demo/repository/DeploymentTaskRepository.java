package com.devops.demo.repository;

import com.devops.demo.model.DeploymentTask;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DeploymentTaskRepository extends JpaRepository<DeploymentTask, Long> {
    List<DeploymentTask> findAllByOrderByCreatedAtDesc();
    List<DeploymentTask> findByStatusIgnoreCase(String status);
    List<DeploymentTask> findByEnvironmentIgnoreCase(String environment);
}
