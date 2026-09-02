package com.devops.demo.config;

import com.devops.demo.model.DeploymentTask;
import com.devops.demo.repository.DeploymentTaskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class DatabaseDataInitializer {

    @Bean
    CommandLineRunner initDatabase(DeploymentTaskRepository repository) {
        return args -> {
            if (repository.count() == 0) {
                repository.saveAll(List.of(
                    new DeploymentTask("auth-service", "v2.1.0", "PROD", "DEPLOYED", "Cloud Build CI/CD"),
                    new DeploymentTask("payment-gateway", "v1.4.2", "STAGING", "IN_PROGRESS", "GitHub Actions"),
                    new DeploymentTask("inventory-api", "v3.0.1", "DEV", "PENDING", "DevOps Admin"),
                    new DeploymentTask("notification-service", "v1.0.0", "PROD", "DEPLOYED", "Cloud Run Serverless")
                ));
            }
        };
    }
}
