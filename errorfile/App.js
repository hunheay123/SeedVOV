import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import BottomTabNavigator from "./components/layout/BottomTabNavigator";
//import Header from "./components/layout/Header";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        //screenOptions={{
        //  header: () => <Header />,
        //}}
      >
        <Stack.Screen
          name="Home"
          component={BottomTabNavigator}
          options={{ headerShown: false }} // 상단 바 안 보이게
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
