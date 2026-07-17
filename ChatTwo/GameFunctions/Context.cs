using System.Text;
using ChatTwo.Util;
using FFXIVClientStructs.FFXIV.Client.UI.Agent;
using FFXIVClientStructs.FFXIV.Client.UI.Info;
using FFXIVClientStructs.FFXIV.Client.UI.Misc;

namespace ChatTwo.GameFunctions;

public sealed unsafe class Context
{
    public static void InviteToNoviceNetwork(string name, ushort world)
    {
        // can specify content id if we have it, but there's no need
        InfoProxyNoviceNetwork.Instance()->InviteToNoviceNetwork(0, 0, world, name.ToTerminatedBytes());
    }

    public static void TryOn(uint itemId, byte stainId)
    {
        AgentTryon.TryOn(0xFF, itemId, stainId);
    }

    public static void LinkItem(uint itemId)
    {
        AgentChatLog.Instance()->LinkItem(itemId);
    }

    public static void LinkStatus(uint statusId)
    {
        AgentChatLog.Instance()->ContextStatusId = statusId;
    }

    public static void OpenItemComparison(uint itemId)
    {
        AgentItemComp.Instance()->CompareItem(0x4D, itemId, 0, 0);
    }

    public static void SearchForRecipesUsingItem(uint itemId)
    {
        AgentRecipeProductList.Instance()->SearchForRecipesUsingItem(itemId);
    }

    public static void SearchForItem(uint itemId)
    {
        ItemFinderModule.Instance()->SearchForItem(itemId);
    }

    public static bool IsDailyRoutinesNpcShopModuleEnabled()
    {
        try
        {
            var ipc = Plugin.Interface.GetIpcSubscriber<string, bool?>("DailyRoutines.IsModuleEnabled");
            return ipc.InvokeFunc("AutoShowItemNPCShopInfo") == true;
        }
        catch
        {
            return false;
        }
    }

    public static void SearchNpcShopSource(uint itemId)
    {
        try
        {
            var ipc = Plugin.Interface.GetIpcSubscriber<uint, bool>(
                "DailyRoutines.Modules.AutoShowItemNPCShopInfo.OpenShopInfoByItemID");
            ipc.InvokeFunc(itemId);
        }
        catch (Exception ex)
        {
            Plugin.Log.Error(ex, "Failed to call DailyRoutines NPC shop source IPC");
        }
    }

    public static void SearchNpcShopDestination(uint itemId)
    {
        try
        {
            var ipc = Plugin.Interface.GetIpcSubscriber<uint, bool>(
                "DailyRoutines.Modules.AutoShowItemNPCShopInfo.OpenExchangeInfoByItemID");
            ipc.InvokeFunc(itemId);
        }
        catch (Exception ex)
        {
            Plugin.Log.Error(ex, "Failed to call DailyRoutines NPC shop destination IPC");
        }
    }

    public static bool IsDailyRoutinesMarketBoardEnabled()
    {
        try
        {
            var ipc = Plugin.Interface.GetIpcSubscriber<string, bool?>("DailyRoutines.IsModuleEnabled");
            return ipc.InvokeFunc("BetterMarketBoard") == true;
        }
        catch
        {
            return false;
        }
    }

    public static void SearchMarketBoard(string itemName)
    {
        var command = $"/pdr market {itemName}";
        var bytes = Encoding.UTF8.GetBytes(command);
        ChatBox.SendMessageUnsafe(bytes);
    }
}
