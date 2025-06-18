using System;
using UnityEngine;
using UnityEngine.Networking;
using Zorro.Core;

public static partial class CloudAPI
{
    public static void CheckVersion(Action<LoginResponse> response)
    {
        GameHandler.AddStatus<QueryingGameTimeStatus>(new QueryingGameTimeStatus());

        string url = "https://raw.githubusercontent.com/KirigiriX/peak-version-data-bypass/refs/heads/main/version.json"; // ⬅️ Replace this with your real GitHub raw URL

        Debug.Log("Sending GET Request to: " + url);

        UnityWebRequest request = UnityWebRequest.Get(url);
        request.SendWebRequest().completed += delegate (AsyncOperation _)
        {
            GameHandler.ClearStatus<QueryingGameTimeStatus>();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.Log("Got error: " + request.error);
                if (request.result != UnityWebRequest.Result.ConnectionError)
                {
                    response?.Invoke(new LoginResponse
                    {
                        VersionOkay = false
                    });
                }
                return;
            }

            string jsonText = request.downloadHandler.text;
            Debug.Log("Got message: " + jsonText);

            LoginResponse loginResponse = JsonUtility.FromJson<LoginResponse>(jsonText);
            response?.Invoke(loginResponse);
        };
    }
}
