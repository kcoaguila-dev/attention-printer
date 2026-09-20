from src.sound_design.logic import get_or_create_whoosh_sfx

def register_sound_design_tools(mcp):
    """
    Registers sound design tools with the provided MCPServer instance.
    """
    @mcp.tool()
    def get_transition_sfx(output_dir: str) -> str:
        """
        Retrieves or synthesizes a clean transition whoosh sound effect (.wav).

        Args:
            output_dir: Directory where the SFX asset will be stored.

        Returns:
            The absolute file path to the transition whoosh audio file.
        """
        return get_or_create_whoosh_sfx(output_dir)
