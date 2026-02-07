package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(HelloController.class)
class HelloControllerTest {

  @Autowired
  MockMvc mvc;

  @Test
  void helloRenders() throws Exception {
    mvc.perform(get("/hello"))
      .andExpect(status().isOk())
      .andExpect(content().string(containsString("Hello World")));
  }
}
