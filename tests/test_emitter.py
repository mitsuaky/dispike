from dispike.eventer import EventHandler
from dispike.models.incoming import IncomingDiscordInteraction
import pytest

event_handler = EventHandler()


@event_handler.on("sampleEvent")
async def dummy_function(*args, **kwargs):
    return kwargs.get("payload")


@event_handler.on("sampleEventDynamicArgs")
async def dummy_dynamic_function(dynamicargument, payload):
    return dynamicargument


@pytest.mark.asyncio
async def test_event_handler():
    assert await event_handler.emit("sampleEvent", payload=True) == True
    assert "sampleEvent" in event_handler.callbacks
    assert event_handler.return_event_settings("sampleEvent") == {}


@pytest.mark.asyncio
async def test_event_handler_fail_no_event():
    with pytest.raises(TypeError):
        await event_handler.return_event_settings("fail")


@pytest.mark.asyncio
async def test_dynamic_arguments_event_handler():
    data = {
        "channel_id": "123123",
        "data": {
            "id": "12312312",
            "name": "sendmessage",
            "options": [{"name": "dynamicargument", "value": "dynamicargumentvalue"}],
        },
        "guild_id": "123123",
        "id": "123123123132",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2019-05-12T18:36:16.878000+00:00",
            "mute": False,
            "nick": None,
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": [
                "123123",
                "123123",
                "1231233",
                "1231233133",
                "12412412414",
            ],
            "user": {
                "avatar": "b723979992a56",
                "discriminator": "3333",
                "id": "234234213122123",
                "public_flags": 768,
                "username": "exo",
            },
        },
        "token": "Null",
        "type": 2,
        "version": 1,
    }

    discord_interaction = IncomingDiscordInteraction(**data)
    dymanic_kwargs = {x.name: x.value for x in discord_interaction.data.options}
    dymanic_kwargs["payload"] = discord_interaction
    assert (
        await event_handler.emit("sampleEventDynamicArgs", **dymanic_kwargs)
        == "dynamicargumentvalue"
    )


def test_non_async_event_handler():
    with pytest.raises(TypeError):

        @event_handler.on("badEvent")
        def test_function(*args, **kwargs):
            return True


@pytest.mark.asyncio
async def test_event_not_existing():
    with pytest.raises(TypeError):
        await event_handler.emit("NotExisting")

    with pytest.raises(TypeError):
        await event_handler.return_event_settings("NotExisting")

    with pytest.raises(TypeError):
        await event_handler.return_event_function("Not Existing")


@pytest.mark.asyncio
async def test_attempt_to_register_multiple_handlers():
    with pytest.raises(TypeError):

        @event_handler.on("duplicateEvent")
        async def dup_one(*args, **kwargs):
            pass

        @event_handler.on("duplicateEvent")
        async def dup_two(*args, **kwargs):
            pass
