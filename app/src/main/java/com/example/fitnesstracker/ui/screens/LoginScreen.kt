package com.example.fitnesstracker.ui.screens

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController

@Composable
fun LoginScreen(navController: NavHostController) {
    Button(onClick = { navController.navigate("dashboard") }) {
        Text("Login")
    }
}