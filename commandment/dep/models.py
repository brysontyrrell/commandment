from commandment.dep import SkipSetupSteps
from commandment.models import db, Certificate, CertificateType
from commandment.dbtypes import GUID


class DEPServerTokenCertificate(Certificate):
    """DEP Server Token Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.STOKEN.value
    }


class DEPConfiguration(db.Model):
    __tablename__ = 'dep_configurations'

    id = db.Column(db.Integer, primary_key=True)
    # certificate for PKI of server token
    certificate_id = db.Column(db.ForeignKey('certificates.id'))
    certificate = db.relationship('DEPServerTokenCertificate', backref='dep_configurations')

    # OAuth creds
    consumer_key = db.String()
    consumer_secret = db.String()
    access_token = db.String()
    access_secret = db.String()

    url = db.String()
    

class DEPAnchorCertificate(Certificate):
    """DEP Anchor Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.ANCHOR.value
    }


class DEPSupervisionCertificate(Certificate):
    """DEP Supervision Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.SUPERVISION.value
    }


dep_profile_anchor_certificates = db.Table(
    'dep_profile_anchor_certificates',
    db.metadata,
    db.Column('dep_profile_id', db.Integer, db.ForeignKey('dep_profiles.id')),
    db.Column('certificate_id', db.Integer, db.ForeignKey('certificates.id')),
)

dep_profile_supervision_certificates = db.Table(
    'dep_profile_supervision_certificates',
    db.metadata,
    db.Column('dep_profile_id', db.Integer, db.ForeignKey('dep_profiles.id')),
    db.Column('certificate_id', db.Integer, db.ForeignKey('certificates.id')),
)


class DEPProfile(db.Model):
    __tablename__ = 'dep_profiles'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(GUID, index=True)
    profile_name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    allow_pairing = db.Column(db.Boolean)
    is_supervised = db.Column(db.Boolean)
    is_multi_user = db.Column(db.Boolean)
    is_mandatory = db.Column(db.Boolean)
    await_device_configured = db.Column(db.Boolean)
    is_mdm_removable = db.Column(db.Boolean)
    support_phone_number = db.Column(db.String)
    auto_advance_setup = db.Column(db.Boolean)
    support_email_address = db.Column(db.String)
    org_magic = db.Column(db.String)
    # skip_setup_items = db.Column(db.Enum(SkipSetupSteps))
    department = db.Column(db.String)

    anchor_certs = db.relationship(
        'DEPAnchorCertificate',
        secondary=dep_profile_anchor_certificates,
        #  back_populates='anchor_dep_profiles'
    )

    supervising_host_certs = db.relationship(
        'DEPSupervisionCertificate',
        secondary=dep_profile_supervision_certificates,
        #  back_populates='supervising_dep_profiles'
    )
