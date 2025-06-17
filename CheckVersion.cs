using System;
using UnityEngine;
using UnityEngine.Networking;
using Zorro.Core;

public static partial class CloudAPI
{
    public static void CheckVersion(Action<LoginResponse> response)
    {
        LoginResponse loginResponse = new LoginResponse
        {
            VersionOkay = true,
            HoursUntilLevel = 1337,
            MinutesUntilLevel = 1337,
            SecondsUntilLevel = 1337,
            LevelIndex = 3,
            Message = "Made with <3 By Kirigiri \nhttps://discord.gg/P5cDx4Fyfc"
        };

        if (response != null)
        {
            response(loginResponse);
        }
    }
}
