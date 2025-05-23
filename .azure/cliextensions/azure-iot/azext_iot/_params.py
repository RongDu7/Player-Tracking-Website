# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
CLI parameter definitions.
"""

from knack.arguments import CLIArgumentType, CaseInsensitiveList
from azure.cli.core.commands.parameters import (
    resource_group_name_type,
    get_enum_type,
    get_resource_name_completion_list,
    get_three_state_flag,
)
from azext_iot.common.shared import (
    EntityStatusType,
    SettleType,
    DeviceAuthType,
    KeyType,
    AttestationType,
    ProtocolType,
    AckType,
    MetricType,
    ReprovisionType,
    AllocationType,
    DistributedTracingSamplingModeType,
    JobType,
    JobCreateType,
    JobStatusType,
    AuthenticationType,
    AuthenticationTypeDataplane,
    RenewKeyType,
)
from azext_iot._validators import mode2_iot_login_handler, process_top
from azext_iot.assets.user_messages import info_param_properties_device


dps_auth_type_dataplane_param_type = CLIArgumentType(
    options_list=["--auth-type"],
    arg_type=get_enum_type(
        AuthenticationTypeDataplane, AuthenticationTypeDataplane.key.value
    ),
    arg_group="Access Control",
    help="Indicates whether the operation should auto-derive a policy key or use the current Azure AD session. "
    "If the authentication type is login and the resource hostname is provided, resource lookup will be skipped unless needed."
    "You can configure the default using `az configure --defaults iotdps-data-auth-type=<auth-type-value>`",
    configured_default="iotdps-data-auth-type",
)

hub_auth_type_dataplane_param_type = CLIArgumentType(
    options_list=["--auth-type"],
    arg_type=get_enum_type(
        AuthenticationTypeDataplane, AuthenticationTypeDataplane.key.value
    ),
    arg_group="Access Control",
    help="Indicates whether the operation should auto-derive a policy key or use the current Azure AD session. "
    "If the authentication type is login and the resource hostname is provided, resource lookup will be skipped unless needed."
    "You can configure the default using `az configure --defaults iothub-data-auth-type=<auth-type-value>`",
    configured_default="iothub-data-auth-type",
)

hub_name_type = CLIArgumentType(
    completer=get_resource_name_completion_list("Microsoft.Devices/IotHubs"),
    help="IoT Hub name.",
)

event_msg_prop_type = CLIArgumentType(
    options_list=["--properties", "--props", "-p"],
    nargs="*",
    choices=CaseInsensitiveList(["sys", "app", "anno", "all"]),
    help="Indicate key message properties to output. "
    "sys = system properties, app = application properties, anno = annotations",
)

children_list_prop_type = CLIArgumentType(
    options_list=["--child-list", "--cl"],
    nargs="*",
    help="Child device list (space separated).",
)

event_timeout_type = CLIArgumentType(
    options_list=["--timeout", "--to", "-t"],
    type=int,
    help="Maximum seconds to maintain connection without receiving message. Use 0 for infinity. ",
)


def load_arguments(self, _):
    """
    Load CLI Args for Knack parser
    """
    with self.argument_context("iot") as context:
        context.argument("resource_group_name", arg_type=resource_group_name_type)
        context.argument(
            "hub_name_or_hostname", options_list=["--hub-name", "-n"], arg_type=hub_name_type,
            help="IoT Hub name or hostname. Required if --login is not provided.",
            arg_group="IoT Hub Identifier"
        )
        context.argument(
            "hub_name", options_list=["--hub-name", "-n"], arg_type=hub_name_type,
            help="IoT Hub name. Required if --login is not provided.",
            arg_group="IoT Hub Identifier"
        )
        context.argument(
            "login",
            options_list=["--login", "-l"],
            validator=mode2_iot_login_handler,
            help="This command supports an entity connection string with rights to perform action. "
            'Use to avoid session login via "az login". '
            "If both an entity connection string and name are provided the connection string takes priority. "
            "Required if --hub-name is not provided.",
            arg_group="IoT Hub Identifier"
        )
        context.argument(
            "device_id", options_list=["--device-id", "-d"], help="Target Device Id."
        )
        context.argument(
            "module_id", options_list=["--module-id", "-m"], help="Target Module Id."
        )
        context.argument(
            "key_type",
            options_list=["--key-type", "--kt"],
            arg_type=get_enum_type(KeyType),
            help="Shared access policy key type for authentication.",
        )
        context.argument(
            "policy_name",
            options_list=["--policy-name", "--pn"],
            help="Shared access policy to use for authentication.",
        )
        context.argument(
            "duration",
            options_list=["--duration", "--du"],
            type=int,
            help="Valid token duration in seconds.",
        )
        context.argument(
            "etag",
            options_list=["--etag", "-e"],
            help="Etag or entity tag corresponding to the last state of the resource. "
            "If no etag is provided the value '*' is used.",
        )
        context.argument(
            "top",
            type=int,
            options_list=["--top"],
            validator=process_top,
            help="Maximum number of elements to return. Use -1 for unlimited.",
        )
        context.argument(
            "method_name",
            options_list=["--method-name", "--mn"],
            help="Target method for invocation.",
        )
        context.argument(
            "method_payload",
            options_list=["--method-payload", "--mp"],
            help="Json payload to be passed to method. Must be file path or raw json.",
        )
        context.argument(
            "method_connect_timeout",
            options_list=["--method-connect-timeout", "--mct"],
            type=int,
            help="Maximum number of seconds to wait on device connection.",
        )
        context.argument(
            "method_response_timeout",
            options_list=["--method-response-timeout", "--mrt"],
            type=int,
            help="Maximum number of seconds to wait for device method result.",
        )
        context.argument(
            "auth_method",
            options_list=["--auth-method", "--am"],
            arg_type=get_enum_type(DeviceAuthType),
            help="The authorization method an entity is to be created with.",
        )
        context.argument(
            "metric_type",
            options_list=["--metric-type", "--mt"],
            arg_type=get_enum_type(MetricType),
            help="Indicates which metric collection should be used to lookup a metric.",
        )
        context.argument(
            "metric_id",
            options_list=["--metric-id", "-m"],
            help="Target metric for evaluation.",
        )
        context.argument(
            "yes",
            options_list=["--yes", "-y"],
            arg_type=get_three_state_flag(),
            help="Skip user prompts. Indicates acceptance of action. "
            "Used primarily for automation scenarios. Default: false",
        )
        context.argument(
            "repair",
            options_list=["--repair", "-r"],
            arg_type=get_three_state_flag(),
            help="Reinstall uamqp dependency compatible with extension version. Default: false",
        )
        context.argument(
            "consumer_group",
            options_list=["--consumer-group", "--cg", "-c"],
            help="Specify the consumer group to use when connecting to event hub endpoint.",
        )
        context.argument(
            "enqueued_time",
            options_list=["--enqueued-time", "--et", "-e"],
            type=int,
            help="Indicates the time that should be used as a starting point to read messages from the partitions. "
            "Units are milliseconds since unix epoch. "
            'If no time is indicated "now" is used.',
        )
        context.argument(
            "content_type",
            options_list=["--content-type", "--ct"],
            help="Specify the Content-Type of the message payload to automatically format the output to that type.",
        )
        context.argument(
            "device_query",
            options_list=["--device-query", "-q"],
            help="Specify a custom query to filter devices.",
        )
        context.argument(
            "edge_enabled",
            options_list=["--edge-enabled", "--ee"],
            arg_type=get_three_state_flag(),
            help="Flag indicating edge enablement.",
        )
        context.argument(
            "connection_string",
            options_list=["--connection-string", "--cs"],
            help="Target connection string. This bypasses the IoT Hub registry and generates the SAS token directly"
            " from the supplied symmetric key without further validation. All other command parameters aside from"
            " duration will be ignored. Supported connection string types: Iot Hub, Device, Module."
        )
        context.argument(
            "custom_metric_queries",
            nargs="+",
            options_list=["--custom-metric-queries", "--cmq"],
            help="An alternative input style (space separated key=value pairs) for --metrics and intended to replace "
            "it in the future. "
            'Format example: metric1="select deviceId from devices where tags.location=\'US\'" metric2="select *"',
        )
        context.argument(
            "custom_labels",
            nargs="+",
            options_list=["--custom-labels", "--cl"],
            help="An alternative input style (space separated key=value pairs) for --labels and intended to replace "
            "it in the future. "
            'Format example: key1=value1 key2="this is my value"',
        )

    with self.argument_context("iot hub") as context:
        context.argument(
            "target_json",
            options_list=["--json", "-j"],
            help="Json to replace existing twin with. Provide file path or raw json.",
        )
        context.argument(
            "policy_name",
            options_list=["--policy-name", "--pn"],
            help="Shared access policy with operation permissions for target IoT Hub entity.",
        )
        context.argument(
            "primary_thumbprint",
            arg_group="X.509",
            options_list=["--primary-thumbprint", "--ptp"],
            help="Self-signed certificate thumbprint to use for the primary thumbprint.",
        )
        context.argument(
            "secondary_thumbprint",
            arg_group="X.509",
            options_list=["--secondary-thumbprint", "--stp"],
            help="Self-signed certificate thumbprint to use for the secondary thumbprint.",
        )
        context.argument(
            "primary_key",
            options_list=["--primary-key", "--pk"],
            help="The primary symmetric shared access key stored in base64 format.",
            arg_group="Symmetric Key",
        )
        context.argument(
            "secondary_key",
            options_list=["--secondary-key", "--sk"],
            help="The secondary symmetric shared access key stored in base64 format.",
            arg_group="Symmetric Key",
        )
        context.argument(
            "valid_days",
            arg_group="X.509",
            options_list=["--valid-days", "--vd"],
            type=int,
            help="Generate self-signed cert and use its thumbprint. Valid "
            "for specified number of days. Default: 365.",
        )
        context.argument(
            "output_dir",
            arg_group="X.509",
            options_list=["--output-dir", "--od"],
            help="Generate self-signed cert and use its thumbprint. "
            "Output to specified target directory",
        )
        context.argument(
            "tags", arg_group="Twin Patch", options_list=["--tags"], help="Twin tags."
        )
        context.argument(
            "desired",
            arg_group="Twin Patch",
            options_list=["--desired"],
            help="Twin desired properties.",
        )
        context.argument(
            "auth_type_dataplane",
            options_list=["--auth-type"],
            arg_type=hub_auth_type_dataplane_param_type,
        )

    with self.argument_context("iot hub invoke-device-method") as context:
        context.argument(
            "timeout",
            options_list=["--timeout", "--to"],
            type=int,
            help="Maximum number of seconds to wait for the device method result.",
        )

    with self.argument_context("iot hub invoke-module-method") as context:
        context.argument(
            "timeout",
            options_list=["--timeout", "--to"],
            type=int,
            help="Maximum number of seconds to wait for the module method result.",
        )

    with self.argument_context("iot hub connection-string") as context:
        context.argument(
            "show_all",
            options_list=["--show-all", "--all"],
            help="Show all shared access policies for the respective IoT Hub.",
        )
        context.argument(
            "default_eventhub",
            arg_type=get_three_state_flag(),
            options_list=["--default-eventhub", "--eh"],
            help="Flag indicating the connection string returned is for the default EventHub endpoint. Default: false.",
        )

    with self.argument_context("iot hub job") as context:
        context.argument("job_id", options_list=["--job-id"], help="IoT Hub job Id.")
        context.argument(
            "job_status",
            options_list=["--job-status", "--js"],
            help="The status of a scheduled job.",
            arg_type=get_enum_type(JobStatusType),
        )
        context.argument(
            "job_type",
            options_list=["--job-type", "--jt"],
            help="The type of scheduled job.",
            arg_type=get_enum_type(JobType),
        )
        context.argument(
            "query_condition",
            options_list=["--query-condition", "-q"],
            help="Condition for device query to get devices to execute the job on. "
            "Required if job type is scheduleDeviceMethod or scheduleUpdateTwin. "
            'Note: The service will prefix "SELECT * FROM devices WHERE " to the input',
        )
        context.argument(
            "start_time",
            options_list=["--start-time", "--start"],
            help="The scheduled start of the job in ISO 8601 date time format. "
            "If no start time is provided, the job is queued for asap execution. "
            "Using a custom start time that's in the past may cause the operation to fail.",
        )
        context.argument(
            "ttl",
            options_list=["--ttl"],
            type=int,
            help="Max execution time in seconds, before job is terminated.",
        )
        context.argument(
            "twin_patch",
            options_list=["--twin-patch", "--patch"],
            help="The desired twin patch. Provide file path or raw json.",
        )
        context.argument(
            "wait",
            options_list=["--wait", "-w"],
            arg_type=get_three_state_flag(),
            help="Block until the created job is in a completed, failed or cancelled state. "
            "Will regularly poll on interval specified by --poll-interval.",
        )
        context.argument(
            "poll_interval",
            options_list=["--poll-interval", "--interval"],
            type=int,
            help="Interval in seconds that job status will be checked if --wait flag is passed in.",
        )
        context.argument(
            "poll_duration",
            options_list=["--poll-duration", "--duration"],
            type=int,
            help="Total duration in seconds where job status will be checked if --wait flag is passed in.",
        )

    with self.argument_context("iot hub job create") as context:
        context.argument(
            "job_type",
            options_list=["--job-type", "--jt"],
            help="The type of scheduled job.",
            arg_type=get_enum_type(JobCreateType),
        )

    with self.argument_context("iot hub monitor-events") as context:
        context.argument("timeout", arg_type=event_timeout_type)
        context.argument("properties", arg_type=event_msg_prop_type)
        context.argument(
            "interface",
            options_list=["--interface", "-i"],
            help="Target interface identifier to filter on. For example: dtmi:com:example:TemperatureController;1",
        )
        context.argument(
            "message_count",
            options_list=["--message-count", "--mc"],
            type=int,
            help="Number of telemetry messages to capture before the monitor is terminated. "
            "If not specified, monitor keeps running until meeting the timeout threshold of not receiving messages from hub.",
        )

    with self.argument_context("iot hub monitor-feedback") as context:
        context.argument(
            "wait_on_id",
            options_list=["--wait-on-msg", "-w"],
            help="Feedback monitor will block until a message with specific id (uuid) is received.",
        )

    with self.argument_context("iot hub device-identity") as context:
        context.argument(
            "status",
            options_list=["--status", "--sta"],
            arg_type=get_enum_type(EntityStatusType),
            help="Set device status upon creation.",
        )
        context.argument(
            "status_reason",
            options_list=["--status-reason", "--star"],
            help="Description for device status.",
        )
        context.argument(
            "device_scope",
            options_list=["--device-scope"],
            help="The scope of the device. "
            "For edge devices, this is auto-generated and immutable. "
            "For leaf devices, set this to create child/parent relationship.",
            arg_group="Device Scope"
        )

    with self.argument_context("iot hub device-identity renew-key") as context:
        context.argument(
            "renew_key_type",
            options_list=["--key-type", "--kt"],
            arg_type=get_enum_type(RenewKeyType),
            help="Target key type to regenerate.",
        )

    with self.argument_context("iot hub device-identity export") as context:
        context.argument(
            "blob_container_uri",
            options_list=["--blob-container-uri", "--bcu"],
            help="Blob Shared Access Signature URI with write, read, and delete access to "
            "a blob container. This is used to output the status of the "
            "job and the results. Note: when using Identity-based authentication an "
            "https:// URI is still required - but no SAS token is necessary. Input for this argument "
            "can be inline or from a file path.",
        )
        context.argument(
            "blob_container_name",
            options_list=["--blob-container", "--bc"],
            help="This blob container is used to output the status of the device identity import job and the results. "
            "Parameter is ignored when blob_container_uri is provided. "
            "Write, read and delete access is required for this blob container.",
        )

        context.argument(
            "storage_account_name",
            options_list=["--storage-account", "--sa"],
            help="Name of Azure Storage account containing the output blob container."
            "Parameter is ignored when blob_container_uri is provided. Write, read and delete access is required.",
        )
        context.argument(
            "include_keys",
            options_list=["--include-keys", "--ik"],
            arg_type=get_three_state_flag(),
            help="If set, keys are exported normally. Otherwise, keys are "
            "set to null in export output.",
        )
        context.argument(
            "storage_authentication_type",
            options_list=["--sat", "--storage-authentication-type"],
            arg_type=get_enum_type(AuthenticationType),
            deprecate_info=context.deprecate(hide=True),
            help="Authentication type for communicating with the storage container.",
        )
        context.argument(
            "identity",
            options_list=["--identity"],
            help="Managed identity type to determine if system assigned managed identity or "
            "user assigned managed identity is used. For system assigned managed identity, use "
            "[system]. For user assigned managed identity, provide the user assigned managed "
            "identity resource id. This identity requires a Storage Blob Data Contributor roles for the Storage "
            "Account.",
        )

    with self.argument_context("iot hub device-identity import") as context:
        context.argument(
            "input_blob_container_uri",
            options_list=["--input-blob-container-uri", "--ibcu"],
            help="Blob Shared Access Signature URI with read access to a blob "
            "container. This blob contains the operations to be performed on "
            "the identity registry. Note: when using Identity-based authentication "
            "an https:// URI is still required - but no SAS token is necessary. Input for this "
            "argument can be inline or from a file path.",
        )
        context.argument(
            "output_blob_container_uri",
            options_list=["--output-blob-container-uri", "--obcu"],
            help="Blob Shared Access Signature URI with write access "
            "to a blob container. This is used to output the status of "
            "the job and the results. Note: when using Identity-based "
            "authentication an https:// URI without the SAS token is still required. "
            "Input for this argument can be inline or from a file path.",
        )
        context.argument(
            "input_blob_container_name",
            options_list=["--input-blob-container", "--ibc"],
            help="This blob container stores the file which defines operations to be performed on the identity registry. "
            "Parameter is ignored when input_blob_container_uri is provided. Read access is required for this blob container.",
        )

        context.argument(
            "input_storage_account_name",
            options_list=["--input-storage-account", "--isa"],
            help="Name of Azure Storage account containing the input blob container."
            "Only required when input_blob_container_uri is not provided. Read access is required.",
        )
        context.argument(
            "output_blob_container_name",
            options_list=["--output-blob-container", "--obc"],
            help="This blob container is used to output the status of the device identity import job and the results. "
            "Only required when input_blob_container_uri is not provided. Write access is required for this blob container.",
        )
        context.argument(
            "output_storage_account_name",
            options_list=["--output-storage-account", "--osa"],
            help="Name of Azure Storage account containing the output blob container."
            "Parameter is ignored when output_blob_container_uri is provided. Write access is required.",
        )
        context.argument(
            "storage_authentication_type",
            options_list=["--sat", "--storage-authentication-type"],
            arg_type=get_enum_type(AuthenticationType),
            deprecate_info=context.deprecate(hide=True),
            help="Authentication type for communicating with the storage container.",
        )
        context.argument(
            "identity",
            options_list=["--identity"],
            help="Managed identity type to determine if system assigned managed identity or "
            "user assigned managed identity is used. For system assigned managed identity, use "
            "[system]. For user assigned managed identity, provide the user assigned managed "
            "identity resource id. This identity requires a Storage Blob Data Contributor role for the target Storage "
            "Account and Contributor role for the IoT Hub.",
        )

    with self.argument_context("iot hub device-identity parent set") as context:
        context.argument(
            "parent_id",
            options_list=["--parent-device-id", "--pd"],
            help="Id of edge device.",
        )
        context.argument(
            "force",
            options_list=["--force", "-f"],
            help="Overwrites the device's parent device.",
        )

    with self.argument_context("iot hub device-identity children") as context:
        context.argument("device_id", help="Id of edge device.")
        context.argument("child_list", arg_type=children_list_prop_type)

    with self.argument_context("iot hub device-identity children add") as context:
        context.argument(
            "force",
            options_list=["--force", "-f"],
            help="Overwrites the child device's parent device.",
        )

    with self.argument_context("iot hub device-identity children remove") as context:
        context.argument(
            "remove_all",
            options_list=["--remove-all", "-a"],
            help="To remove all children.",
        )

    with self.argument_context("iot hub module-identity renew-key") as context:
        context.argument(
            "renew_key_type",
            options_list=["--key-type", "--kt"],
            arg_type=get_enum_type(RenewKeyType),
            help="Target key type to regenerate.",
        )

    with self.argument_context("iot hub distributed-tracing update") as context:
        context.argument(
            "sampling_mode",
            options_list=["--sampling-mode", "--sm"],
            help="Turns sampling for distributed tracing on and off. 1 is On and, 2 is Off.",
            arg_type=get_enum_type(DistributedTracingSamplingModeType),
        )
        context.argument(
            "sampling_rate",
            options_list=["--sampling-rate", "--sr"],
            help="Controls the amount of messages sampled for adding trace context. This value is"
            "a percentage. Only values from 0 to 100 (inclusive) are permitted.",
        )

    with self.argument_context("iot hub query") as context:
        context.argument(
            "query_command",
            options_list=["--query-command", "-q"],
            help="User query to be executed.",
        )
        context.argument(
            "top",
            options_list=["--top"],
            type=int,
            help="Maximum number of elements to return. By default query has no cap.",
        )

    with self.argument_context("iot device") as context:
        context.argument(
            "auth_type_dataplane",
            options_list=["--auth-type"],
            arg_type=hub_auth_type_dataplane_param_type,
        )
        context.argument(
            "data",
            options_list=["--data", "--da"],
            help="Message body for text or raw json."
        )
        context.argument(
            "data_file_path",
            options_list=["--data-file-path", "--dfp"],
            is_preview=True,
            help="""Provide path to file for message body payload. Please note when the payload needs
            to be sent in binary format, set the content type to application/octet-stream."""
        )
        context.argument(
            "properties",
            options_list=["--properties", "--props", "-p"],
            help=info_param_properties_device(),
        )
        context.argument(
            "msg_count",
            options_list=["--msg-count", "--mc"],
            type=int,
            help="Number of device messages to send to IoT Hub.",
        )
        context.argument(
            "msg_interval",
            options_list=["--msg-interval", "--mi"],
            type=int,
            help="Delay in seconds between device-to-cloud messages.",
        )
        context.argument(
            "receive_settle",
            options_list=["--receive-settle", "--rs"],
            arg_type=get_enum_type(SettleType),
            help="Indicates how to settle received cloud-to-device messages. "
            "Supported with HTTP only.",
        )
        context.argument(
            "protocol_type",
            options_list=["--protocol", "--proto"],
            arg_type=get_enum_type(ProtocolType),
            help="Indicates device-to-cloud message protocol",
        )

    with self.argument_context("iot device simulate") as context:
        context.argument(
            "properties",
            options_list=["--properties", "--props", "-p"],
            help=info_param_properties_device(include_http=True),
        )
        context.argument(
            "method_response_code",
            type=int,
            options_list=["--method-response-code", "--mrc"],
            help="Status code to be returned when direct method is executed on device. Optional param, only supported for mqtt.",
        )
        context.argument(
            "method_response_payload",
            options_list=["--method-response-payload", "--mrp"],
            help="Payload to be returned when direct method is executed on device. Provide file path or raw json. "
            "Optional param, only supported for mqtt.",
        )
        context.argument(
            "init_reported_properties",
            options_list=["--init-reported-properties", "--irp"],
            help="Initial state of twin reported properties for the target device when the simulator is run. "
            "Optional param, only supported for mqtt.",
        )

    with self.argument_context("iot device c2d-message") as context:
        context.argument(
            "correlation_id",
            options_list=["--correlation-id", "--cid"],
            help="The correlation Id associated with the C2D message.",
        )
        context.argument(
            "properties",
            options_list=["--properties", "--props", "-p"],
            help=info_param_properties_device(include_mqtt=False),
        )
        context.argument(
            "expiry_time_utc",
            options_list=["--expiry-time-utc", "--expiry"],
            type=int,
            help="Units are milliseconds since unix epoch. "
            "If no time is indicated the default IoT Hub C2D message TTL is used.",
        )
        context.argument(
            "message_id",
            options_list=["--message-id", "--mid"],
            help="The C2D message Id. If no message Id is provided a UUID will be generated.",
        )
        context.argument(
            "user_id",
            options_list=["--user-id", "--uid"],
            help="The C2D message, user Id property.",
        )
        context.argument(
            "lock_timeout",
            options_list=["--lock-timeout", "--lt"],
            type=int,
            help="Specifies the amount of time a message will be invisible to other receive calls.",
        )
        context.argument(
            "content_type",
            options_list=["--content-type", "--ct"],
            help="The content type for the C2D message body.",
        )
        context.argument(
            "content_encoding",
            options_list=["--content-encoding", "--ce"],
            help="The encoding for the C2D message body.",
        )

    with self.argument_context("iot device c2d-message send") as context:
        context.argument(
            "ack",
            options_list=["--ack"],
            arg_type=get_enum_type(AckType),
            help="Request the delivery of per-message feedback regarding the final state of that message. "
            "The description of ack values is as follows. "
            "Positive: If the c2d message reaches the Completed state, IoT Hub generates a feedback message. "
            "Negative: If the c2d message reaches the Dead lettered state, IoT Hub generates a feedback message. "
            "Full: IoT Hub generates a feedback message in either case. "
            "By default, no ack is requested.",
        )
        context.argument(
            "wait_on_feedback",
            options_list=["--wait", "-w"],
            arg_type=get_three_state_flag(),
            help="If set the c2d send operation will block until device feedback has been received.",
        )

    with self.argument_context("iot device c2d-message receive") as context:
        context.argument(
            "abandon",
            arg_group="Message Ack",
            options_list=["--abandon"],
            arg_type=get_three_state_flag(),
            help="Abandon the cloud-to-device message after receipt.",
        )
        context.argument(
            "complete",
            arg_group="Message Ack",
            options_list=["--complete"],
            arg_type=get_three_state_flag(),
            help="Complete the cloud-to-device message after receipt.",
        )
        context.argument(
            "reject",
            arg_group="Message Ack",
            options_list=["--reject"],
            arg_type=get_three_state_flag(),
            help="Reject the cloud-to-device message after receipt.",
        )

    with self.argument_context("iot device upload-file") as context:
        context.argument(
            "file_path",
            options_list=["--file-path", "--fp"],
            help="Path to file for upload.",
        )
        context.argument(
            "content_type",
            options_list=["--content-type", "--ct"],
            help="MIME Type of file.",
        )

    with self.argument_context("iot hub configuration") as context:
        context.argument(
            "config_id",
            options_list=["--config-id", "-c"],
            help="Target device configuration name. Lowercase and the following special characters are allowed: [-+%_*!'].",
        )
        context.argument(
            "target_condition",
            options_list=["--target-condition", "--tc", "-t"],
            help="Target condition in which a device or module configuration applies to. "
            "Configurations with no target condition will target no device or module. "
            "Use the following format: \"tags.environment='test'\".",
        )
        context.argument(
            "priority",
            options_list=["--priority", "--pri"],
            help="Weight of the device configuration in case of competing rules (highest wins).",
        )
        context.argument(
            "content",
            options_list=["--content", "-k"],
            help="Device configuration content. Provide file path or raw json.",
        )
        context.argument(
            "metrics",
            options_list=["--metrics", "-m"],
            help="Device configuration metric definitions. Provide file path or raw json."
            "Using --custom-metric-queries instead of --metrics is recommended.",
        )
        context.argument(
            "labels",
            options_list=["--labels", "--lab"],
            help="Map of labels to be applied to target configuration. "
            "Using --custom-labels instead of --labels is recommended."
            'Format example: {"key0":"value0", "key1":"value1"}',
        )
        context.argument(
            "top",
            options_list=["--top"],
            type=int,
            help="Maximum number of configurations to return. By default all configurations are returned.",
        )

    with self.argument_context("iot edge") as context:
        context.argument(
            "config_id",
            options_list=["--deployment-id", "-d"],
            help="Target deployment name. Lowercase and the following special characters are allowed: [-+%_*!'].",
        )
        context.argument(
            "target_condition",
            options_list=["--target-condition", "--tc", "-t"],
            help="Target condition in which an edge deployment applies to. Deployments with no target condition "
            "will target no device. Use the following format: \"tags.environment='test'\".",
        )
        context.argument(
            "priority",
            options_list=["--priority", "--pri"],
            help="Weight of deployment in case of competing rules (highest wins).",
        )
        context.argument(
            "content",
            options_list=["--content", "-k"],
            help="IoT Edge deployment content. Provide file path or raw json.",
        )
        context.argument(
            "metrics",
            options_list=["--metrics", "-m"],
            help="IoT Edge deployment user metric definitions. Provide file path or raw json. "
            'User metrics are in the form of {"queries":{...}} or {"metrics":{"queries":{...}}}. '
            "Using --custom-metric-queries instead of --metrics is recommended.",
        )
        context.argument(
            "labels",
            options_list=["--labels", "--lab"],
            help="Map of labels to be applied to target deployment. "
            'Use the following format: \'{"key0":"value0", "key1":"value1"}\'. '
            "Using --custom-labels instead of --labels is recommended.",
        )
        context.argument(
            "top",
            options_list=["--top"],
            type=int,
            help="Maximum number of deployments to return. By default all deployments are returned.",
        )
        context.argument(
            "layered",
            options_list=["--layered"],
            arg_type=get_three_state_flag(),
            help="Layered deployments allow you to define desired properties in $edgeAgent, $edgeHub and user "
            "modules that will layer on top of a base deployment. The properties specified in a layered "
            "deployment will merge with properties of the base deployment. Properties with the same path will be "
            "overwritten based on deployment priority. This option is an alias for --no-validation.",
        )
        context.argument(
            "no_validation",
            options_list=["--no-validation"],
            arg_type=get_three_state_flag(),
            help="Disables client side schema validation for edge deployment creation.",
        )
        context.argument(
            "auth_type_dataplane",
            options_list=["--auth-type"],
            arg_type=hub_auth_type_dataplane_param_type,
        )

    with self.argument_context("iot dps") as context:
        context.argument(
            "login",
            options_list=["--login", "-l"],
            validator=mode2_iot_login_handler,
            help="This command supports an entity connection string with rights to perform action. "
            'Use to avoid session login via "az login". '
            "If both an entity connection string and name are provided the connection string takes priority. "
            "Required if --dps-name is not provided.",
            arg_group="Device Provisioning Service Identifier"
        )
        context.argument(
            "dps_name",
            options_list=["--dps-name", "-n"],
            help="Name or hostname of the Azure IoT Hub Device Provisioning Service. Required if --login is not provided.",
            arg_group="Device Provisioning Service Identifier"
        )
        context.argument(
            "initial_twin_properties",
            options_list=["--initial-twin-properties", "--props"],
            help="Initial device twin properties.",
        )
        context.argument(
            "initial_twin_tags",
            options_list=["--initial-twin-tags", "--tags"],
            help="Initial device twin tags.",
        )
        context.argument(
            "iot_hub_host_name",
            options_list=["--iot-hub-host-name", "--hn"],
            deprecate_info=context.deprecate(redirect="--iot-hubs", hide=True),
            help="Host name of target IoT Hub. Allocation policy defaults to static if this parameter is provided.",
        )
        context.argument(
            "provisioning_status",
            options_list=["--provisioning-status", "--ps"],
            arg_type=get_enum_type(EntityStatusType),
            help="Enable or disable enrollment entry.",
        )
        context.argument(
            "certificate_path",
            options_list=["--certificate-path", "--cp"],
            help="The path to the file containing the primary certificate.",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_certificate_path",
            options_list=["--secondary-certificate-path", "--scp"],
            help="The path to the file containing the secondary certificate.",
            arg_group="Authentication"
        )
        context.argument(
            "remove_certificate",
            options_list=["--remove-certificate", "--rc"],
            help="Flag to remove current primary certificate.",
            arg_type=get_three_state_flag(),
            arg_group="Authentication"
        )
        context.argument(
            "remove_secondary_certificate",
            options_list=["--remove-secondary-certificate", "--rsc"],
            help="Flag to remove current secondary certificate.",
            arg_type=get_three_state_flag(),
            arg_group="Authentication"
        )
        context.argument(
            "reprovision_policy",
            options_list=["--reprovision-policy", "--rp"],
            arg_type=get_enum_type(ReprovisionType),
            help="Policy to determine how device data should be handled on re-provision to a different IoT Hub.",
        )
        context.argument(
            "allocation_policy",
            options_list=["--allocation-policy", "--ap"],
            arg_type=get_enum_type(AllocationType),
            help="Type of allocation policy to determine how a device is assigned to an IoT Hub. If not "
            "provided, the allocation policy will be the current allocation policy default set for the "
            "Device Provisioning Service instance.",
            arg_group="Allocation Policy"
        )
        context.argument(
            "iot_hubs",
            options_list=["--iot-hubs", "--ih"],
            help="Host name of target IoT Hub associated with the allocation policy. Use space-separated "
            "list for multiple IoT Hubs.",
            nargs="+",
            action="extend",
            arg_group="Allocation Policy"
        )
        context.argument(
            "webhook_url",
            options_list=["--webhook-url", "--wh"],
            help="The Azure Function webhook URL used for custom allocation requests.",
            arg_group="Allocation Policy"
        )
        context.argument(
            "api_version",
            options_list=["--api-version", "--av"],
            help="The API version of the provisioning service types sent in the custom allocation"
            " request. Minimum supported version: 2018-09-01-preview.",
            arg_group="Allocation Policy"
        )
        context.argument(
            "auth_type_dataplane",
            options_list=["--auth-type"],
            arg_type=dps_auth_type_dataplane_param_type,
        )

    with self.argument_context("iot dps compute-device-key") as context:
        context.argument(
            "enrollment_id",
            options_list=["--enrollment-id", "--eid", "--group-id", "--gid"],
            help="Enrollment group ID."
        )
        context.argument(
            "symmetric_key",
            options_list=["--symmetric-key", "--key"],
            help="The symmetric shared access key for the enrollment group. This bypasses the "
            "Device Provisioning Service registry and generates the SAS token directly "
            "from the supplied symmetric key without further validation. All other command "
            "parameters aside from registration ID will be ignored.",
        )
        context.argument("registration_id", help="ID of device registration. ")

    with self.argument_context("iot dps connection-string") as context:
        context.argument(
            "show_all",
            options_list=["--show-all", "--all"],
            help="Show all shared access policies for the respective DPS.",
        )

    with self.argument_context("iot dps enrollment") as context:
        context.argument(
            "enrollment_id",
            options_list=["--enrollment-id", "--eid"],
            help="Individual device enrollment ID."
        )
        context.argument("device_id", help="Device ID registered in the IoT Hub.")
        context.argument(
            "primary_key",
            options_list=["--primary-key", "--pk"],
            help="The primary symmetric shared access key stored in base64 format. ",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_key",
            options_list=["--secondary-key", "--sk"],
            help="The secondary symmetric shared access key stored in base64 format. ",
            arg_group="Authentication"
        )
        context.argument(
            "device_information",
            options_list=["--device-information", "--info"],
            help="Optional device information.",
        )

    with self.argument_context("iot dps enrollment create") as context:
        context.argument(
            "attestation_type",
            options_list=["--attestation-type", "--at"],
            arg_type=get_enum_type(AttestationType),
            help="Attestation Mechanism used for authentication to the DPS.",
            arg_group="Authentication"
        )
        context.argument(
            "certificate_path",
            options_list=["--certificate-path", "--cp"],
            help="The path to the file containing the primary certificate. "
            "Required when choosing x509 as attestation type and the secondary"
            " certificate path is not provided.",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_certificate_path",
            options_list=["--secondary-certificate-path", "--scp"],
            help="The path to the file containing the secondary certificate. "
            "Required when choosing x509 as attestation type and the primary"
            " certificate path is not provided.",
            arg_group="Authentication"
        )
        context.argument(
            "endorsement_key",
            options_list=["--endorsement-key", "--ek"],
            help="TPM endorsement key for a TPM device. "
            "When choosing tpm as attestation type, endorsement key is required.",
            arg_group="Authentication"
        )

    with self.argument_context("iot dps enrollment show") as context:
        context.argument(
            "show_keys",
            options_list=["--show-keys", "--keys"],
            arg_type=get_three_state_flag(),
            help="Include attestation keys and information in enrollment results.",
        )

    with self.argument_context("iot dps enrollment update") as context:
        context.argument(
            "endorsement_key",
            options_list=["--endorsement-key", "--ek"],
            help="TPM endorsement key for a TPM device.",
        )

    with self.argument_context("iot dps enrollment registration") as context:
        context.argument(
            "registration_id",
            options_list=["--enrollment-id", "--eid"],
            help="Individual device enrollment ID."
        )

    with self.argument_context("iot dps enrollment-group") as context:
        context.argument(
            "enrollment_id",
            options_list=["--enrollment-id", "--eid", "--group-id", "--gid"],
            help="Enrollment group ID."
        )
        context.argument(
            "primary_key",
            options_list=["--primary-key", "--pk"],
            help="The primary symmetric shared access key stored in base64 format. ",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_key",
            options_list=["--secondary-key", "--sk"],
            help="The secondary symmetric shared access key stored in base64 format. ",
            arg_group="Authentication"
        )
        context.argument(
            "certificate_path",
            options_list=["--certificate-path", "--cp"],
            help="The path to the file containing the primary certificate. "
            "If attestation with an intermediate certificate is desired then a certificate path must be provided.",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_certificate_path",
            options_list=["--secondary-certificate-path", "--scp"],
            help="The path to the file containing the secondary certificate. "
            "If attestation with an intermediate certificate is desired then a certificate path must be provided.",
            arg_group="Authentication"
        )
        context.argument(
            "root_ca_name",
            options_list=["--root-ca-name", "--ca-name", "--cn"],
            help="The name of the primary root CA certificate. "
            "If attestation with a root CA certificate is desired then a root ca name must be provided.",
            arg_group="Authentication"
        )
        context.argument(
            "secondary_root_ca_name",
            options_list=["--secondary-root-ca-name", "--secondary-ca-name", "--scn"],
            help="The name of the secondary root CA certificate. "
            "If attestation with a root CA certificate is desired then a root ca name must be provided.",
            arg_group="Authentication"
        )
        context.argument(
            "registration_id",
            options_list=["--registration-id", "--rid"],
            help="ID of device registration."
        )

    with self.argument_context("iot dps enrollment-group show") as context:
        context.argument(
            "show_keys",
            options_list=["--show-keys", "--keys"],
            arg_type=get_three_state_flag(),
            help="Include attestation keys and information in enrollment group results.",
        )

    with self.argument_context("iot dps enrollment-group compute-device-key") as context:
        context.argument(
            "symmetric_key",
            options_list=["--symmetric-key", "--key"],
            help="The symmetric shared access key for the enrollment group. This bypasses the "
            "Device Provisioning Service registry and generates the SAS token directly "
            "from the supplied symmetric key without further validation. All other command "
            "parameters aside from registration ID will be ignored.",
        )

    with self.argument_context("iot dps registration") as context:
        context.argument("registration_id", help="ID of device registration.")

    with self.argument_context("iot dps registration list") as context:
        context.argument(
            "enrollment_id",
            options_list=["--enrollment-id", "--eid", "--group-id", "--gid"],
            help="Enrollment group ID."
        )
