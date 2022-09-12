__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from minecraft_manager.main import create_app
from minecraft_manager.db import db
from minecraft_manager.models.common.game_system import GameSystem, GameSystemFacetDatum, GameSystemImageDatum
from minecraft_manager.models.initiative.condition import Condition, ConditionHealthAdjustment
from minecraft_manager.models.initiative.encounter import Encounter, EncounterParticipant, EncounterParticipantGroup, EncounterParticipantHealthDatum, EncounterParticipantMetrics, EncounterParticipantTurnData, EncounterRegion, EncounterSession, EncounterSessionTimelineEntry
from minecraft_manager.models.initiative.group import EncounterGroup
from minecraft_manager.models.initiative.participant import Participant, ParticipantGroup, ParticipantHealthDatum
from minecraft_manager.models.initiative.tracked_encounter import TrackedEncounter
from minecraft_manager.models.user import User, Identity, Role, Permission, UserRole
from minecraft_manager.models.profile import Profile
from minecraft_manager.models.entitlement import Entitlement, EntitlementGrant

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

# provide a migration utility command
manager.add_command('db', MigrateCommand)

# enable python shell with application context


@manager.shell
def shell_ctx():
    return dict(app=app,
                db=db,
                User=User, Identity=Identity, Role=Role, Profile=Profile, Permission=Permission, UserRole=UserRole,
                Entitlement=Entitlement, EntitlmentGrant=EntitlementGrant,
                GameSystem=GameSystem, GameSystemFacetDatum=GameSystemFacetDatum, GameSystemImageDatum=GameSystemImageDatum,
                Condition=Condition, ConditionHealthAdjustment=ConditionHealthAdjustment,
                Encounter=Encounter, EncounterParticipant=EncounterParticipant, EncounterParticipantGroup=EncounterParticipantGroup, EncounterParticipantHealthDatum=EncounterParticipantHealthDatum, EncounterParticipantMetrics=EncounterParticipantMetrics, EncounterParticipantTurnData=EncounterParticipantTurnData, EncounterRegion=EncounterRegion, EncounterSession=EncounterSession, EncounterSessionTimelineEntry=EncounterSessionTimelineEntry,
                EncounterGroup=EncounterGroup,
                Participant=Participant, ParticipantGroup=ParticipantGroup, ParticipantHealthDatum=ParticipantHealthDatum,
                TrackedEncounter=TrackedEncounter)


if __name__ == '__main__':
    manager.run()
