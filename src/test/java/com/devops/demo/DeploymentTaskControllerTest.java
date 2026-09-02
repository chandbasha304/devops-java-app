package com.devops.demo;

import com.devops.demo.model.DeploymentTask;
import com.devops.demo.repository.DeploymentTaskRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class DeploymentTaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private DeploymentTaskRepository repository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setup() {
        repository.deleteAll();
    }

    @Test
    void shouldCreateAndRetrieveDeploymentTask() throws Exception {
        DeploymentTask task = new DeploymentTask("order-service", "v1.0.0", "PROD", "DEPLOYED", "Cloud Build");

        // 1. Create (POST)
        String response = mockMvc.perform(post("/api/v1/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(task)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", notNullValue()))
                .andExpect(jsonPath("$.serviceName", is("order-service")))
                .andExpect(jsonPath("$.status", is("DEPLOYED")))
                .andReturn().getResponse().getContentAsString();

        DeploymentTask createdTask = objectMapper.readValue(response, DeploymentTask.class);

        // 2. Get All (GET)
        mockMvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].serviceName", is("order-service")));

        // 3. Update (PUT)
        createdTask.setStatus("FAILED");
        mockMvc.perform(put("/api/v1/tasks/" + createdTask.getId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(createdTask)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("FAILED")));

        // 4. Delete (DELETE)
        mockMvc.perform(delete("/api/v1/tasks/" + createdTask.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.deleted", is(true)));
    }
}
