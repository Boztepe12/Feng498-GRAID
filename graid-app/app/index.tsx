import { ThemedText } from "@/components/ThemedText";
import { Stack } from "expo-router";
import { Text, View } from "react-native";
import { useState, useEffect } from 'react';

import * as Location from "expo-location";


export default function Index() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setErrorMsg("Permission to access location was denied");
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);
    })();
  }, []);

  return (
    <>
      <Stack.Screen options={{ title: "Home" }} />
      <View
        style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        
        {
          errorMsg ? <ThemedText>{errorMsg}</ThemedText> : location ? <ThemedText>{JSON.stringify(location)}</ThemedText> : <ThemedText>Loading...</ThemedText>
        }
        <ThemedText>Edit app/index.tsx to edit this screen.</ThemedText>
      </View>
    </>
  );
}
