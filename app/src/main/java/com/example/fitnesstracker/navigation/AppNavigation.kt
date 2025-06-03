package com.example.fitnesstracker.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.fitnesstracker.ui.screens.DashboardScreen
import com.example.fitnesstracker.ui.screens.LoginScreen

@Composable
fun AppNavigation(navController: NavHostController) {
    NavHost(navController, startDestination = "login") {
        composable("login") { LoginScreen(navController) }
        composable("dashboard") { DashboardScreen(navController) }
    }
}